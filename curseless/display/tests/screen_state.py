class FakeTerminal:
    '''
    A class for performing state-based testing.
    '''
    def __init__(self):
        self.is_dirty = False
        self.is_drawn = False

    def move(self, y, x):
        self.is_dirty = True

    def addstr(self, y, x, text, style=None):
        self.is_dirty = True

    def refresh(self):
        self.is_drawn = True
