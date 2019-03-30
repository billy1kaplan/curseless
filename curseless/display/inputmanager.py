from .reader import Reader


class InputManager:
    @staticmethod
    def from_stdin(loop, executor):
        return InputManager(Reader(loop, executor))

    def __init__(self, reader):
        """
        key_register: Callable[Callable[[code], None], None]
        A callback to register with <= the register calls this on
        key press
        """
        self.callback = None
        self.reader = reader
        reader.register(self.handle_input)

    def handle_input(self, code):
        if self.callback:
            self.callback(code)

    def add_handler(self, handler):
        self.callback = handler

    def remove_handler(self, handler):
        self.callback = None

    def shutdown(self):
        self.reader.shutdown()
