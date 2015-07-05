import sys
sys.path.append('..')

from nose.plugins.skip import SkipTest
from nose.plugins.attrib import attr
import os.path
import unittest
import codecs
from nyctext import nycaddress as parser


class ParseExpectations(unittest.TestCase):

    def __init__(self, *args, **kwds):
        super(ParseExpectations, self).__init__(*args, **kwds)
        self.datadir = os.path.join(os.path.dirname(__file__), 'data')

    def checkExpectation(self, sample, expect, verbose=False):
        source = os.path.join(self.datadir, sample)
        expectation = os.path.join(self.datadir, expect)

        expected = open(expectation).readlines()
        expected = [e.strip() for e in expected]

        text = codecs.open(source, 'r', encoding='utf8').read()
        addresses = parser.parse(text, verbose)

        if verbose:
            print 'expect:\t'
            if isinstance(expected, list):
                print
                for e in expected:
                    print '\t%s' % e
            else:
                print '%s' % expected
            print
            print 'got \t:'
            if isinstance(addresses, list):
                print
                for e in addresses:
                    print '\t%s' % e
            else:
                print '%s' % addresses

        for loc in addresses:
            self.assertIn(loc, expected)
            expected.remove(loc)

        self.assertEqual(expected, [])