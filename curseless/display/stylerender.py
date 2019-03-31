from curseless.location import Location
from .styles import HIGHLIGHT


class StyleTextRenderer:
    def __init__(self, display):
        self.display = display

    def text(self, text, offset, style):
        y_max, x_max = self.display.dimensions()
        width, height = self._max_width(text), self._height(text)
        location = style.determine_location(offset,
                                            y_max,
                                            x_max,
                                            width,
                                            height)

        self._render_fill(location, x_max, height, style.fill)
        self.display.render_text(location, text, style=style.get_styles())

    def clear(self, text, offset, style):
        y_max, x_max = self.display.dimensions()
        width, height = self._max_width(text), self._height(text)
        location = style.determine_location(offset,
                                            y_max,
                                            x_max,
                                            width,
                                            height)
        for i in range(height):
            self.display.render_text(location.plus(Location(y=i)), ' ' * width)

    def _max_width(self, text):
        return max([len(line) for line in text.split('\n')])

    def _height(self, text):
        return text.count('\n') + 1

    def dimensions(self):
        return self.display.dimensions()

    def draw(self, focus):
        self.display.draw(focus)

    def _render_fill(self, location, width, height, fill):
        if not fill:
            return

        for i in range(height):
            self.display.render_text(location.plus(Location(y=i)),
                                     ' ' * (width - 1),
                                     style=HIGHLIGHT)
