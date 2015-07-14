# Todo build a more comprehensive list of throughways.
# See: http://www.semaphorecorp.com/cgi/abbrev.html
# have to treat broadway & bowery as a thhoroughfare
# because they are valid street names and thoroughfares in of
# themselves

names = [
    'avenue',
    'boulevard',
    'bowery',
    'broadway',
    'circle',
    'concourse',
    'crescent',
    'drive',
    'expressway',
    'highway',
    'lane',
    'loop',
    'park',
    'piers',
    'place',
    'plaza',
    'road',
    'slip',
    'square',
    'street',
    'terrace',
    'turnpike',
]

names = '|'.join(names)
names = '(%s)' % names
