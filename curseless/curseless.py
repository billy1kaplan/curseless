import asyncio

from .location import Location
from .diff import diff_render


class Curseless:
    """
    Class that represents the unidirectional from of data.

    Model -> View -> Update -> Model -> ...

    This class observes messages from the view to feed to the
    update function,
    """
    def __init__(self, model, update, view, display, subs=[]):
        self.model = model
        self.update = update
        self.view = view
        self.subs = subs
        self.display = display

    def run(self):
        """
        Starts the render loop as well as async subscriptions
        """
        self.render(self.model)

        tasks = [sub(self) for sub in self.subs]
        asyncio.gather(*tasks)

    def notify(self, msg):
        """ Observes messages and rerenders as appropriate """
        old_view = self.view(self.model)
        new_model = self.update(msg, self.model)
        self.model = new_model
        new_view = self.view(new_model)
        diff_render(Location(), old_view, new_view, self.display, self)
        self.display.draw()

    def render(self, model):
        displayable = self.view(model)
        displayable.render(Location(), self.display, self)
        self.display.draw()
