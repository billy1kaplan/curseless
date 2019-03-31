import unittest

from ..screen import Display
from ...location import Location

from .screen_state import FakeTerminal


class TestScreen(unittest.TestCase):
    def setUp(self):
        self.mock = FakeTerminal()
        self.sut = Display.without_styles(self.mock)

    def test_draw_screen(self):
        self.sut.draw(Location())
        self.assertTrue(self.mock.is_drawn)

    def test_add_text(self):
        self.sut.render_text(Location(), 'Sample text', None)
        self.assertTrue(self.mock.is_dirty)

    def test_add_text_with_style(self):
        self.sut.render_text(Location(), 'Sample text', ['Some made up style'])
        self.assertTrue(self.mock.is_dirty)
