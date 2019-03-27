import unittest

from ..location import Location


class TestLocation(unittest.TestCase):
    def test_add_locations(self):
        loc1 = Location(x=1, y=2)
        loc2 = Location(x=3, y=2)

        expected = Location(x=4, y=4)

        self.assertEqual(loc1.plus(loc2), expected)

    def test_add_locations_1(self):
        loc1 = Location(x=-1, y=-5)
        loc2 = Location(x=6, y=8)

        expected = Location(x=5, y=3)

        self.assertEqual(loc1.plus(loc2), expected)


if __name__ == '__main__':
    unittest.main()
