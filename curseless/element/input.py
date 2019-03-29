class InputNode:
    """
    A node for text input.
    """
    noop_key = lambda x, y, z: None

    def __init__(self, location, echo=True, on_key=noop_key):
        self.location = location
        self.echo = echo
        self.on_key = on_key

    def render(self, offset, renderer, observer):
        def wrap(*args, **kwargs):
            observer.notify(self.on_key(*args, **kwargs))
        renderer.add_input(self, self.location.plus(offset), wrap, self.echo)

    def clear(self, offset, renderer, observer):
        renderer.update(offset.plus(self.location), ' ' * 100, '')
