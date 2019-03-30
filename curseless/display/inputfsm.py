from .keycodes import CTLC, RET, TAB, LEFT, RIGHT, DEL, UP, DOWN


class InputFSM:
    @staticmethod
    def fromText(text):
        lines = text.split('\n')
        return InputFSM(lines=text.split('\n'), index=len(lines[-1]), span=len(lines))

    """ A state machine for keeping track of an individual text input """
    def __init__(self, lines=[''], index=0, span=0):
        self.lines = lines
        self.index = index
        self.span = span

    def update(self, text):
        self.lines = text.split('\n')
        self.index = len(self.lines[-1])
        self.span = len(self.lines) - 1

    def insert(self, char):
        line = self.span
        cur_line = self.lines[line]
        new_line = cur_line[:self.index] + char + cur_line[self.index:]
        self.lines[line] = new_line

    # Delete and return deleted character (if there is one)
    def _delete(self):
        if self.index == 0 and self.span == 0:
            return

        if self.index == 0:
            line = self.lines.pop(self.span)
            self.lines[self.span - 1] += line

        cur_line = self.lines[self.span]
        new_line = cur_line[:self.index-1] + cur_line[self.index:]
        self.lines[self.span] = new_line
        self.index -= 1

    def clear(self):
        self.lines = ['']
        self.index = 0
        self.span = 0

    def _receive_return(self):
        self.lines.insert(self.span + 1, '')
        self.index = 0
        self.span += 1

    def _walk_left(self):
        if self.index == 0 and self.span > 0:
            self.span -= 1
            self.index = len(self.lines[self.span])
        elif self.index > 0:
            self.index -= 1

    def _walk_right(self):
        line_len = len(self.lines[self.span])
        if self.index == line_len - 1 and self.span < len(self.lines):
            self.index = 0
            self.span += 1
        elif self.index < line_len and line_len != 0:
            self.index += 1

    def _insert(self, char):
        self.insert(char)
        self.index += 1

    def receive_input(self, code):
        if code == CTLC:
            return
        elif code == TAB:
            return
        elif code == RET:
            self._receive_return()
        elif code == DEL:
            self._delete()
        elif code == LEFT:
            self._walk_left()
        elif code == RIGHT:
            self._walk_right()
        elif code == UP or code == DOWN:
            pass
        else:
            self._insert(code)

    def text(self):
        return '\n'.join(self.lines)

    def __str__(self):
        return '\n'.join(self.lines)
