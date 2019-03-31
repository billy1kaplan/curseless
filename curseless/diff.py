from .element.composite import CompositeNode
from .element.input import InputNode
from .element.textnode import TextNode


def diff_render(location, old, new, display, observer):
    """
    Renders nodes as needed
    TODO: Way to different input nodes. Maybe we can hash them?
          (hash the callback function, text, style, location, etc.)
          and then rerender on change
    """
    clear_queue, render_queue = [], []

    def similar_composite(c1, c2):
        return len(c1.nodes) == len(c2.nodes) and c1.location == c2.location

    def diff(location, old, new):
        def append_diff():
            clear_queue.append(lambda:
                               old.clear(location, display, observer))

            render_queue.append(lambda:
                                new.render(location, display, observer))

        if isinstance(old, InputNode) and isinstance(new, InputNode):
            pass
        elif isinstance(old, CompositeNode) and isinstance(new, CompositeNode):
            if similar_composite(old, new):
                for node1, node2 in zip(old.nodes, new.nodes):
                    diff(location.plus(old.location), node1, node2)
            else:
                append_diff()
        elif isinstance(old, TextNode) and isinstance(new, TextNode):
            if old.text != new.text or old.style != new.style:
                append_diff()
        else:
            append_diff()

    diff(location, old, new)

    # Clear everything first before rendering
    # or this ends up looking like swiss cheese
    for node in clear_queue:
        node()

    for node in render_queue:
        node()
