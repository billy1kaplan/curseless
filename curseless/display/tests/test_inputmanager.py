import unittest
from unittest.mock import Mock

from ..inputmanager import InputManager


class TestInputManager(unittest.TestCase):
    def setUp(self):
        self.input_manager = InputManager(lambda x: x)

    def test_calls_callback(self):
        mock = Mock()
        self.input_manager.add_handler(mock)
        self.input_manager.handle_input('A')
        mock.assert_called_once()

    def test_removes_callback(self):
        mock = Mock()
        self.input_manager.add_handler(mock)
        self.input_manager.handle_input('A')
        mock.assert_called_once()

        self.input_manager.remove_handler()
        self.input_manager.handle_input('A')
        mock.assert_called_once()
