from typing import Callable, Union, Any, List, Tuple, NamedTuple

from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode

from curseless.location import Location
from curseless.message import Message

from curseless.display.keycodes import RET, LEFT, RIGHT, UP, DOWN


Select = Message[Tuple[str, List[any]]]('SELECT')
Options = Message[List[any]]('UPDATE')
Choose = Message[int]('CHOOSE')


class Model(NamedTuple):
    selected: int = 0


Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    if Select.matches(msg):
        char, options = Select.retrieve_payload(msg)

        if char in [LEFT, UP, 'k']:
            direction = -1
        elif char in [RIGHT, DOWN, 'j']:
            direction = 1
        else:
            direction = 0

        return model._replace(selected=(model.selected + direction)
                              % len(options))
    elif Options.matches(msg):
        options = Options.retrieve_payload(msg)
        return model._replace(selected=min(model.selected,
                                           max(0,
                                               len(options) - 1)))
    else:
        return model


def clear(code, text):
    return ''


def make_menu(options, model, handler):
    def make_item(option, i):
        if i == model.selected:
            prompt = '> '
            return CompositeNode(Location(y=i),
                                 [TextNode(Location(), prompt),
                                  CompositeNode(Location(x=len(prompt)),
                                                [option]),
                                  InputNode(Location(
                                      x=len(prompt) + len(option.text)),
                                            on_key=handler,
                                            transformer=clear,
                                            echo=False)])
        else:
            return CompositeNode(Location(y=i), [option])

    return [make_item(option, i) for i, option in enumerate(options)]


Node = Union[TextNode, InputNode, CompositeNode]


def Menu(options, model: Model,
         intercept=lambda ch: None,
         offset=Location()) -> Node:
    def key_handler(ch, text):
        intercept_msg = intercept(ch)
        if intercept_msg is not None:
            return intercept_msg.make_message(model.selected)

        if ch == RET:
            return Choose.make_message(model.selected)
        else:
            return Select.make_message((ch, options))

    return CompositeNode(offset, make_menu(options, model, key_handler))
