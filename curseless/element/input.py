class InputNode:
    """
    A node for text input.
    """
    def noop_key(key, text):
        return None

    def noop_id(key, text):
        return text

    def __init__(self,
                 location,
                 echo=True,
                 on_key=noop_key,
                 transformer=noop_id):
        self.location = location
        self.echo = echo
        self.on_key = on_key
        self.transformer = transformer

    def render(self, offset, renderer, observer):
        def wrap(*args, **kwargs):
            observer.notify(self.on_key(*args, **kwargs))
        renderer.add_input(self.location.plus(offset), '',
                           on_key=wrap,
                           echo=self.echo,
                           transformer=self.transformer)
        renderer.focus_update(self.location.plus(offset))

    def clear(self, offset, renderer, observer):
        renderer.update(offset.plus(self.location), ' ' * 100, '', None)
        renderer.clear_input(self)
