from curseless.location import Location
from .inputfsm import InputFSM
from .style import Style


class Terminal:
    def __init__(self, input_manager, display, focus=Location()):
        self.input_manager = input_manager
        self.display = display
        self.focus = focus

    def focus_update(self, focus):
        self.focus = focus

    def wrapper(self,
                location,
                callback,
                echo,
                transformer=lambda code, text: text):
        fsm = InputFSM()

        def closure(code):
            old_text = fsm.text()
            transformed = transformer(code, old_text)
            if transformed != old_text:
                fsm.update(transformed)
            else:
                fsm.receive_input(code)

            if echo:
                self.focus = Location(x=location.x + fsm.index, y=location.y)
                self.update(location, old_text, fsm.text(), style=None)
                self.display.draw(self.focus)

            callback(code, old_text)

        return closure

    def add_input(self, location, text, on_key, echo, **kwargs):
        self.input_manager.add_handler(
            self.wrapper(location, on_key, echo, **kwargs)
        )

    def text(self, location: Location, text: str, style) -> None:
        if not style:
            style = Style()
        self.display.text(text, location, style)

    def update(self,
               location: Location,
               old_text: str,
               text: str,
               style) -> None:
        if style is None:
            style = Style()
        self.display.clear(old_text, location, style)
        self.display.text(text, location, style)

    def clear_input(self, handler):
        self.input_manager.remove_handler(handler)

    def draw(self):
        self.display.draw(self.focus)
