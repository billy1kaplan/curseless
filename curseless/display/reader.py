import sys

import threading

from .keycodes import CTLC, RET, TAB, LEFT, RIGHT, DEL, UP, DOWN


class Reader:
    """
    A keyboard reader that translates inputs into either a printable
    ascii character or into a command code.
    """

    def __init__(self, loop, executor):
        self.loop = loop
        self.executor = executor
        self.stoprequest = threading.Event()

    def register(self, call_back):
        """ Registers a call_back on the keyboard input.

        A seperate thread is spun up to run the keyboard listener and
        then the callback is executed synchronously in the original thread.

        Parameters
        ----------
        call_back : code -> None
            The callback to be called upon receiving keyboard input
        """
        def sync_callback(*args, **kwargs):
            self.loop.call_soon_threadsafe(call_back, *args, **kwargs)
        self.loop.run_in_executor(self.executor,
                                  self._key_reader,
                                  sync_callback)

    def shutdown(self):
        self.stoprequest.set()

    def _key_reader(self, call_back):
        while not self.stoprequest.isSet():
            char = ord(sys.stdin.read(1))

            if char == 3:
                call_back(CTLC)
                return
            elif 32 <= char <= 126:
                call_back(chr(char))
            elif char == 9:
                call_back(TAB)
            elif char in {10, 13}:
                call_back(RET)
            elif char == 27:
                next1, next2 = ord(sys.stdin.read(1)), ord(sys.stdin.read(1))
                if next1 == 91 or next1 == 79:
                    if next2 == 68:
                        call_back(LEFT)
                    elif next2 == 67:
                        call_back(RIGHT)
                    elif next2 == 66:
                        call_back(DOWN)
                    elif next2 == 65:
                        call_back(UP)
            elif char == 127:
                call_back(DEL)
