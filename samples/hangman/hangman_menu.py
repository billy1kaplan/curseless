from typing import Callable, Union, Any, List, Tuple, NamedTuple

from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode
from curseless.location import Location

from curseless.display.style import Style
from curseless.display.styles import ALIGN_CENTER

from curseless.message import Message

from .. import menu


class Model(NamedTuple):
    menu: menu.Model
    options: List[str] = ['Start Game', 'How to Play', 'High Scores']


initial_model: Model = Model(menu=menu.Model())
Start = Message[None]('START_GAME')


def generate_menu(menu):
    options = menu.options
    return [TextNode(Location(), node) for node in options]


Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    if menu.Select.matches(msg):
        return model._replace(menu=menu.update(msg, model.menu))
    elif menu.Choose.matches(msg):
        return model._replace(menu=menu.update(msg, model.menu))
    else:
        return model


Node = Union[TextNode, InputNode, CompositeNode]


def view(model: Model) -> Node:
    center = Style(x_rel=ALIGN_CENTER)
    welcome_text = 'The deranged game where guessing' +\
        'a letter wrong brings you one body part closer to doom'
    return CompositeNode(Location(), [
                TextNode(Location(y=5), 'Welcome to hangman', style=center),
                TextNode(Location(y=6), welcome_text, style=center),
                menu.Menu(generate_menu(model), model.menu)
            ])
