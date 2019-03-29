import unittest

from ..inputfsm import InputFSM
from ..keycodes import RET, LEFT, RIGHT, DEL


class TestInputFSM(unittest.TestCase):
    def setUp(self):
        self.fsm = InputFSM()

    def test_add_characters(self):
        self.fsm.receive_input('A')
        self.fsm.receive_input('B')
        self.fsm.receive_input('C')

        expected = 'ABC'

        self.assertEqual(self.fsm.text(), expected)
        self.assertEqual(self.fsm.index, len(expected))
        self.assertEqual(self.fsm.span, 0)

    def test_initial_text(self):
        input_text = 'sample'
        fsm = InputFSM.fromText(input_text)

        fsm.receive_input('A')
        self.assertEqual(fsm.text(), input_text + 'A')
        self.assertEqual(fsm.index, len(input_text) + 1)
        self.assertEqual(fsm.span, 0)

    def test_add_newlines(self):
        self.fsm.clear()
        self.fsm.receive_input(RET)

        self.assertEqual(self.fsm.text(), '\n')
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 1)

    def test_delete_empty(self):
        self.fsm.clear()
        self.fsm.receive_input(DEL)
        self.assertEqual(self.fsm.text(), '')
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 0)

    def test_delete(self):
        self.fsm.clear()
        self.fsm = InputFSM.fromText('123')
        self.fsm.receive_input(DEL)
        self.assertEqual(self.fsm.text(), '12')
        self.assertEqual(self.fsm.index, 2)
        self.assertEqual(self.fsm.span, 0)

    def test_cursor_left_empty(self):
        self.fsm.clear()
        self.fsm.receive_input(LEFT)
        self.assertEqual(self.fsm.text(), '')
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 0)

    def test_cursor_right_empty(self):
        self.fsm.clear()
        self.fsm.receive_input(RIGHT)
        self.assertEqual(self.fsm.text(), '')
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 0)

    def test_add_new_line_and_text(self):
        self.fsm.clear()
        self.fsm.receive_input(RET)
        self.fsm.receive_input('A')
        self.assertEqual(self.fsm.text(), '\nA')
        self.assertEqual(self.fsm.index, 1)
        self.assertEqual(self.fsm.span, 1)

    def test_movement(self):
        self.fsm.clear()
        self.fsm.receive_input(RET)
        self.fsm.receive_input('A')
        self.fsm.receive_input(RET)
        self.fsm.receive_input('B')
        self.fsm.receive_input(RET)

        self.assertEqual(self.fsm.text(), '\nA\nB\n')
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 3)

        self.fsm.receive_input(LEFT)
        self.assertEqual(self.fsm.index, 1)
        self.assertEqual(self.fsm.span, 2)

        self.fsm.receive_input(LEFT)
        self.assertEqual(self.fsm.index, 0)
        self.assertEqual(self.fsm.span, 2)

        self.fsm.receive_input(LEFT)
        self.assertEqual(self.fsm.index, 1)
        self.assertEqual(self.fsm.span, 1)

        self.fsm.receive_input(LEFT)
        self.fsm.receive_input(DEL)
        self.assertEqual(self.fsm.text(), 'A\nB\n')
