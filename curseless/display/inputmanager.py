from .reader import Reader


class InputManager:
    @staticmethod
    def from_stdin():
        return InputManager(Reader())

    def __init__(self, key_register):
        """
        key_register: Callable[Callable[[code], None], None]
        A callback to register with <= the register calls this on
        key press
        """
        self.callback = None

        key_register(self.handle_input)

    def handle_input(self, code):
        if self.callback:
            self.callback(code)

    def add_handler(self, handler):
        self.callback = handler

    def remove_handler(self, handler):
        self.callback = None
