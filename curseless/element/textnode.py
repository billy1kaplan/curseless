class TextNode:
    """
    Represents some text
    """
    def __init__(self, location, text, style=None):
        self.location = location
        self.text = text
        self.style = style

    def render(self, offset, renderer, observer):
        renderer.text(self.location.plus(offset), self.text, self.style)

    def clear(self, offset, renderer, observer):
        renderer.update(self.location.plus(offset), self.text, '', self.style)
