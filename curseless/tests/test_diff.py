import unittest
from unittest.mock import Mock

from ..location import Location
from ..diff import diff_render
from ..element.textnode import TextNode


class TestDiffRender(unittest.TestCase):
    def setUp(self):
        self.display = Mock()
        self.observer = Mock()

    def test_compare_text(self):
        t1 = TextNode(Location(), 'some text')
        t2 = t1

        diff_render(Location(), t1, t2, self.display, self.observer)
        self.display.assert_not_called()

    def test_diff_text(self):
        t1 = TextNode(Location(), 'text1')
        t2 = TextNode(Location(), 'text2')

        diff_render(Location(), t1, t2, self.display, self.observer)
        self.display.text.assert_called_once()
        self.display.update.assert_called_once()
