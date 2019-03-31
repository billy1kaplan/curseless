import curses
from collections import defaultdict
from functools import reduce

from typing import Dict, List, Union

from curseless.location import Location
from .styles import HIGHLIGHT, DIM, DEFAULT, RED, GREEN


Style = Union[str, List[str]]


class Display:
    '''
    For handling text display
    '''
    @staticmethod
    def with_standard_attributes(screen):
        '''
        Factory method for constructing the display with
        styles as described in the styles file
        '''
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        attrs = defaultdict(int, {
            HIGHLIGHT: curses.A_STANDOUT,
            DIM: curses.A_DIM,
            DEFAULT: 0,
            RED: curses.color_pair(1),
            GREEN: curses.color_pair(2)
        })

        return Display(screen, attrs)

    @staticmethod
    def without_styles(screen):
        return Display(screen, defaultdict(int))

    def __init__(self, screen, attrs: Dict[str, int]) -> None:
        '''
        screen is an external API for manipulating output
        '''
        self.screen = screen
        self.attrs = attrs

    def render_text(self, loc: Location, text: str, style: Style = DEFAULT):
        '''
        Takes a chunk of text and renders it on the terminal at a given
        location with a particular style.

        Parameters:
        loc : specifies the absolute location to render the text
        text : the text to display on screen
        style : a constant that specifies the style of the rendered string
        '''
        lines = text.split('\n')
        display_style = self._mix_styles(style)

        for i, line in enumerate(lines):
            self.screen.addstr(loc.y + i, loc.x, line, display_style)

    def _mix_styles(self, style: Style) -> int:
        if not style or isinstance(style, str):
            return self.attrs[style]
        return reduce(lambda acc, cur: acc | self.attrs[cur], style, 0)

    def dimensions(self):
        """
        Returns dimensions in the form (y, x)
        """
        return self.screen.getmaxyx()

    def draw(self, focus: Location) -> None:
        '''
        Actually performs the screen redraw and the terminal display to
        refresh.

        Parameters:
        focus : the location where the cursor is moved to
        '''
        self.screen.move(focus.y, focus.x)
        self.screen.refresh()
