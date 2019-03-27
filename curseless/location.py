from typing import NamedTuple


class Location(NamedTuple):
    """ Represents a 2D location """
    x: int = 0
    y: int = 0

    def plus(self, other):
        """ Adds two locations together
        Parameters
        ----------
        other : Location -> Location
            Another location to add this one to
        :return: returns the combination of these two locations
        """
        return Location(x=self.x + other.x, y=self.y + other.y)
