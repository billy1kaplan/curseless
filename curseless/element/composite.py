class CompositeNode:
    """
    A node composed of several child nodes. Applies the location offset to all
    children.
    """
    def __init__(self, location, nodes):
        self.nodes = nodes
        self.location = location

    def render(self, offset, renderer, observer):
        for node in self.nodes:
            node.render(self.location.plus(offset), renderer, observer)

    def clear(self, offset, renderer, observer):
        for node in self.nodes:
            node.clear(self.location.plus(offset), renderer, observer)
