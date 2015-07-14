from ..expectations import ParseExpectations


class Saint(ParseExpectations):
    '''Addresses with Occupancy tags
    '''

    def __init__(self, *args, **kwds):
        super(Saint, self).__init__(*args, **kwds)

    def testStreet(self):
        'St expands to saint'

        source = "DoSomething.org: 19 St Johns Pl. Brooklyn, NY"
        expected = "19 Saint Johns Place Brooklyn, NY"
        expected = [expected]

        self.checkExpectation(source, expected, True)

    def testStreet(self):
        'St expands to saint'

        source = "130 St. Edwards St. Brooklyn, NY"
        expected = "130 Saint Edwards Street Brooklyn, NY"
        expected = [expected]

        self.checkExpectation(source, expected, True)
