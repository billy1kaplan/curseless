from typing import Callable, Union, Any, List, Tuple, NamedTuple

from curseless.entry import run
from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode
from curseless.message import Message
from curseless.location import Location
from curseless.display.style import Style
from curseless.display.styles import ALIGN_RIGHT
from curseless.display.keycodes import RET
from curseless.clock import clock

import random
import sys


class Model(NamedTuple):
    tip: str
    ideas: List[str]
    clock: int
    topic: str = 'Anonymous brainstorming session'


helpful_tips = [
    'Quantity > Perceived Quality',
    'Don\'t think "no but...", think "Yes and..."!',
    'Defer Judgement. All ideas are good!',
    'Be wild',
    'Empathize',
    'Maybe the aliens can solve your problems?',
]


def init_model(topic):
    if topic is None:
        return Model(tip=random.choice(helpful_tips),
                     ideas=[],
                     clock=30)
    else:
        return Model(topic=topic,
                     tip=random.choice(helpful_tips),
                     ideas=[],
                     clock=30)


Tick = Message[None]('TICK')
AddIdea = Message[str]('ADD_IDEA')
Noop = Message[None]('NOOP')
Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    if Tick.matches(msg):
        if model.clock % 4 == 0:
            return model._replace(clock=model.clock - 1,
                                  tip=random.choice(helpful_tips))
        else:
            return model._replace(clock=model.clock - 1)

    elif AddIdea.matches(msg):
        idea = AddIdea.retrieve_payload(msg)

        if idea not in model.ideas:
            return model._replace(ideas=model.ideas + [idea])
        else:
            return model

    else:
        return model


def list_ideas(model):
    return '\n'.join(' - ' + idea for idea in model.ideas)


Node = Union[TextNode, InputNode, CompositeNode]


def view(model: Model) -> Node:
    if model.clock <= 0:
        return CompositeNode(Location(), [
            TextNode(Location(),
                     'Great job! Here are some of your best ideas :)'),
            TextNode(Location(y=2), list_ideas(model))
        ])

    def handle(key, text):
        if key == RET:
            return AddIdea.make_message(text)
        else:
            return Noop.make_message()

    def clear_on_enter(key, text):
        if key == RET:
            return ''
        else:
            return text

    prompt = '> '
    return CompositeNode(Location(), [
        TextNode(Location(), model.topic),
        TextNode(Location(y=2), prompt),
        InputNode(Location(x=len(prompt), y=2),
                  on_key=handle,
                  transformer=clear_on_enter),
        TextNode(Location(y=3), list_ideas(model)),
        TextNode(Location(), 'Time Left: ' + str(model.clock), style=Style(
            y_rel=ALIGN_RIGHT,
        )),
        TextNode(Location(), model.tip, style=Style(
            x_rel=ALIGN_RIGHT,
        )),
    ])


def main():
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = None

    timer = clock(1, Tick)
    run(model=init_model(topic),
        update=update,
        view=view,
        subs=[timer])


if __name__ == '__main__':
    main()
