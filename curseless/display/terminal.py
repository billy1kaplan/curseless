from curseless.location import Location
from .input_machine import InputFSM


class Terminal:
    def __init__(self, input_manager, display, focus=Location()):
        self.input_manager = input_manager
        self.display = display
        self.focus = focus

    def focus_update(self, focus):
        self.focus = focus

    def wrapper(self, location, callback, echo):
        fsm = InputFSM()

        def closure(code):
            old_text = fsm.text
            fsm.receive_input(code)
            callback(fsm.text)

            if echo:
                self.focus = Location(x=location.x + fsm.index, y=location.y)
                self.display.update(location, old_text, fsm.text())
                self.display.draw()

        return closure

    def add_input(self, location, text, on_key, echo):
        self.input_manager.add_handler(self.wrapper(location, on_key, echo))

    def text(self, location: Location, text: str, style) -> None:
        self.display.text(location, text, style)

    def update(self, location: Location, old_text, text: str, style) -> None:
        self.display.update(location, old_text, text, style)

    def clear_input(self):
        self.input_manager.remove_handler()
