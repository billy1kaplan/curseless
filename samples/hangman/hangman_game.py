from typing import Callable, Union, Any, List, Tuple, NamedTuple

from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode

from curseless.location import Location

from curseless.message import Message

from .drawings import drawings
from .word_gen import choose_word


class Model(NamedTuple):
    guessed: List
    clock: int
    max_guesses: int
    word: str


Tick = Message[None]('TICK')
Restart = Message[None]('RESTART')
Guess = Message[str]('GUESS')


generate_game: Callable[[], Model]
generate_game: Model = lambda: Model(guessed=[],
                                     clock=30,
                                     max_guesses=drawings['lives'],
                                     word=choose_word())

Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    if Tick.matches(msg):
        return model._replace(clock=model.clock - 1)

    elif Guess.matches(msg):
        guess = Guess.retrieve_payload(msg)

        if guess not in model.guessed and guess.isalpha() and len(guess) == 1:
            return model._replace(guessed=model.guessed + [guess])
        else:
            return model
    else:
        return model


def display_word(word, guesses):
    return ''.join([x if x in guesses else '*' for x in word])


def won(model):
    return len(set(model.word) - set(model.guessed)) == 0


def guesses(model):
    return len(set(model.guessed) - set(model.word))


def lost(model):
    return guesses(model) >= model.max_guesses or model.clock <= 0


Node = Union[TextNode, InputNode, CompositeNode]


def view(model: Model) -> Node:
    if won(model):
        return CompositeNode(Location(), [
            InputNode(Location(y=10),
                      on_key=lambda ch, text: Restart.make_message(ch),
                      echo=False),
            TextNode(Location(y=0), 'You win! Congrats you ' + model.word),
            TextNode(Location(y=2), 'Press Enter to Restart')
        ])

    if lost(model):
        return CompositeNode(Location(), [
            TextNode(Location(y=0), 'You lose!'),
            InputNode(Location(y=3),
                      on_key=lambda ch, text: Restart.make_message(ch),
                      echo=False),
            TextNode(Location(y=1), 'The word was: ' + model.word),
            TextNode(Location(y=2), 'Press Enter to Restart'),
        ])

    def handle(key, text):
        return Guess.make_message(key)
    return CompositeNode(Location(), [
        TextNode(Location(y=1), display_word(model.word, model.guessed)),
        InputNode(Location(y=2),
                  on_key=handle,
                  transformer=lambda ch, text: '',
                  echo=False),
        TextNode(Location(y=3), 'Time Left: ' + str(model.clock)),
        TextNode(Location(y=4), ''.join(model.guessed)),
        TextNode(Location(y=6), drawings['background']),
        TextNode(Location(x=1, y=9), drawings[guesses(model)]),
    ])
