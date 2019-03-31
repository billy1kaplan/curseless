import unittest

from ..message import Message


class TestMessage(unittest.TestCase):
    def test_matches(self):
        Test = Message('TEST')
        msg = Test.make_message()

        self.assertTrue(Test.matches(msg))

    def test_retrieve(self):
        Test = Message('TEST')
        text = 'hi'
        msg = Test.make_message(text)

        self.assertEqual(Test.retrieve_payload(msg), text)
