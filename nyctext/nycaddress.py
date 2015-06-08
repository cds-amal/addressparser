# -*- coding: utf-8 -*-
__author__ = "C. Sudama, Matthew Alhonte"
__credits__ = ["Mikael Hveem", ]
__license__ = "Apache License 2.0: http://www.apache.org/licenses/LICENSE-2.0"


import os
import nltk
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk-data'))
from nltk.tokenize import sent_tokenize

import re

import usaddress

from reflocation import RefLocation
from nyc_geoclient import Geoclient
from tagger import chunkAddresses

def showFailureReason(msg, address, components, verbose=False):
    if verbose:
        print 'Failed: %s' % msg
        print '\tAddress:\t\t%s' % address
        print '\tUS Address Components:\t%s\n' % components


def location_to_string(tree):
    return ' '.join([c[0] for c in tree]).replace(' ,', ',')


def probableAddresses(text, verbose=False):
    locations = []
    sentences = sent_tokenize(text)
    for s in sentences:
        if verbose:
            print '\n\n'
            print '=' * 48
            print 'Sentence: %s\n' % s
        if len(s) < 10:
            if verbose:
                showFailureReason('Sentence too short', s, '--', verbose)
            continue
        locs = chunkAddresses(s, verbose)
        locations += locs

    return locations


def isValidAddress(ady, verbose=False):

    address = usaddress.parse(ady)
    if len(address) < 4:
        showFailureReason('Not Enough Terms', ady, address, verbose)
        return False

    if any([a[1] == 'Recipient' for a in address]):
        showFailureReason('Recipient', ady, address, verbose)
        return False

    if not any([a[1] == 'StreetName' for a in address]):
        showFailureReason('StreetName', ady, address, verbose)
        return False

    if not any([a[1] == 'AddressNumber' for a in address]):
        showFailureReason('AddressNumber', ady, address, verbose)
        return False

    return True


def lookup_geo(g, ady, verbose=False):
    if verbose:
        print 'Lookup_geo:\n\t%s' % ady

    components = usaddress.parse(ady)
    tags, _ = usaddress.tag(ady)

    addressNumber = tags.get('AddressNumber', '')
    streetName = '%s %s' % (tags.get('StreetName', ''), tags.get('StreetNamePostType', ' '))
    borough = tags.get('PlaceName', '').lower()

    # Todo - map neighborhoods to boroughs
    # ie: long island city -> queens
    #
    if borough == 'ny':
        borough = 'manhattan'

    if borough == 'long island city':
        borough = 'queens'

    if verbose:
        print usaddress.tag(ady)
        print 'adNumber: %s\t\tstName: %s\t\tBorough:%s' % (addressNumber, streetName, borough)
        print

    dic = g.address(addressNumber, streetName, borough)
    zipcode = dic.get('zipCode', '')
    streetAddress = '%s %s' % (dic.get('houseNumber', ''),
                               dic.get('firstStreetNameNormalized', ''))

    borough = dic.get('firstBoroughName', '')
    longitude = dic.get('longitude', '')
    latitude = dic.get('latitude', '')

    place = RefLocation(streetAddress, borough, zipcode, latitude, longitude)
    return place.schema_object()


def parse(text, verbose=False):
    candidates = probableAddresses(text, verbose)
    candidates = [location_to_string(c) for c in candidates]

    # only candidates that end in NY
    rex = re.compile('(.+,\s+NY)', re.IGNORECASE)
    candidates = [rex.match(c) for c in candidates]
    candidates = [c.group() for c in candidates if c is not None]

    return [c for c in candidates if isValidAddress(c)]


def parse_with_geo(text, g, verbose=False):
    plains = parse(text, verbose)
    res = [lookup_geo(g, p) for p in plains]
    return res

if __name__ == '__main__':
    import codecs
    from os import environ

    # https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    appid = environ['DOITT_CROL_APP_ID']
    appkey = environ['DOITT_CROL_APP_KEY']

    sample = codecs.open('../tests/ad-sample1.txt', 'r', encoding='utf8') \
        .read()

    g = Geoclient(appid, appkey)
    for address in parse(sample):
        print 'Address: %s' % address
        print lookup_geo(g, address)
        print