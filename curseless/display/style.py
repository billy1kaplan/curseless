from .styles import DEFAULT, ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT
from curseless.location import Location


class Style:
    def __init__(self,
                 x_rel=ALIGN_LEFT,
                 y_rel=ALIGN_LEFT,
                 style=DEFAULT,
                 fill=False):
        self.x_rel = x_rel
        self.y_rel = y_rel
        self.style = style
        self.fill = fill

    def _determine_rel_offset(self, val, max_val, align, size):
        if align == ALIGN_LEFT:
            return val
        elif align == ALIGN_CENTER:
            return max_val // 2 - size // 2 + val
        elif align == ALIGN_RIGHT:
            return max_val - size - val - 1
        else:
            return val

    def determine_location(self, location, y_max, x_max, width, height):
        x = self._determine_rel_offset(location.x, x_max, self.x_rel, width)
        y = self._determine_rel_offset(location.y, y_max, self.y_rel, height)
        return Location(x=x, y=y)

    def get_styles(self):
        return self.style

    def __str__(self):
        return f'style={self.style}, align={self.x_rel}, {self.y_rel}'
