from typing import Callable, Union, Any, Tuple, NamedTuple

from enum import Enum

from curseless.entry import run
from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode
from curseless.display.keycodes import RET
from curseless.clock import clock

from . import hangman_menu
from . import hangman_game
from .. import menu


class State(Enum):
    MENU = 'MENU'
    IN_GAME = 'IN_GAME'


class Model(NamedTuple):
    state: State
    data: Union[hangman_menu.Model, hangman_game.Model]


options = ['Start Game', 'How to Play', 'High Scores']


initial_model: Model = Model(state=State.MENU,
                             data=hangman_menu.Model(menu=menu.Model(),
                                                     options=options))


Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    key, data = msg
    if menu.Choose.matches(msg):
        choice = menu.Choose.retrieve_payload(msg)
        if model.data.options[choice] == 'Start Game':
            return model._replace(state=State.IN_GAME,
                                  data=hangman_game.generate_game())
        else:
            return model

    elif hangman_game.Restart.matches(msg):
        char = hangman_game.Restart.retrieve_payload(msg)
        if char == RET:
            return Model(state=State.IN_GAME,
                         data=hangman_game.generate_game())
        else:
            return model

    elif model.state == State.MENU and menu.Select.matches(msg):
        return model._replace(data=hangman_menu.update(msg, model.data))

    elif model.state == State.IN_GAME and (
            hangman_game.Guess.matches(msg)
            or hangman_game.Tick.matches(msg)):
        return model._replace(data=hangman_game.update(msg, model.data))

    else:
        return model


Node = Union[TextNode, InputNode, CompositeNode]


def view(model: Model) -> Node:
    if model.state == State.MENU:
        return hangman_menu.view(model.data)
    elif model.state == State.IN_GAME:
        return hangman_game.view(model.data)


def main():
    timer = clock(1, hangman_game.Tick)

    run(model=initial_model,
        update=update,
        view=view,
        subs=[timer])


if __name__ == '__main__':
    main()
