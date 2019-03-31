from typing import NamedTuple, List, Tuple, Callable, Any, Union

from curseless.entry import run

from curseless.element.input import InputNode
from curseless.element.composite import CompositeNode
from curseless.element.textnode import TextNode

from curseless.message import Message
from curseless.location import Location

from curseless.display.style import Style
from curseless.display.styles import (DIM,
                                      DEFAULT,
                                      HIGHLIGHT,
                                      ALIGN_RIGHT,
                                      GREEN,
                                      ALIGN_CENTER)

from curseless.display.keycodes import RET, TAB

from .. import menu


class Todo(NamedTuple):
    task: str
    completed: bool = False


class Model(NamedTuple):
    todos: List[Todo]
    menu: menu.Model
    adding: bool = True


initial_model: Model = Model(todos=[],
                             menu=menu.Model())

# Message:
Press = Message[Tuple[str, Callable[[], None]]]('PRESS')
Swap = Message[None]('SWAP')
Noop = Message[None]('NOOP')
Del = Message[int]('DEL')
Toggle = Message[int]('TOGGLE')

Msg = Tuple[str, Any]
Update = Callable[[Msg, Model], Model]


def update(msg: Msg, model: Model) -> Model:
    key, data = msg

    if Press.matches(msg):
        todo = Press.retrieve_payload(msg)
        return model._replace(todos=model.todos + [Todo(todo)])
    elif Swap.matches(msg):
        return model._replace(adding=not model.adding or len(model.todos) == 0)
    elif Del.matches(msg):
        index = Del.retrieve_payload(msg)
        todos = [todo for i, todo in enumerate(model.todos) if i != index]
        return model._replace(todos=todos,
                              adding=len(todos) == 0,
                              menu=menu.update(
                                  menu.Options.make_message(todos),
                                  model.menu))
    elif Toggle.matches(msg):
        index = Toggle.retrieve_payload(msg)
        todos = [todo if i != index else Todo(task=todo.task,
                                              completed=not todo.completed)
                 for i, todo in enumerate(model.todos)]
        return model._replace(todos=todos)
    elif menu.Select.matches(msg):
        return model._replace(menu=menu.update(msg, model.menu))
    else:
        return model


def render_todo(i, todo, prefix, space):
    if todo.completed:
        style = Style(style=[GREEN, DIM])
    else:
        style = Style(style=DEFAULT)
    if space:
        return TextNode(Location(y=i), prefix + todo.task, style=style)
    else:
        return TextNode(Location(), prefix + todo.task, style=style)


def render_todos(todos, prefix, space):
    return [render_todo(i, todo, prefix, space)
            for i, todo in enumerate(todos)]


def list_todos(location, model, prefix='- ', space=True):
    return CompositeNode(location, render_todos(model.todos, prefix, space))


def input_todo(location, model):
    def handle(key, text):
        if key == RET:
            return Press.make_message(text)
        elif key == TAB:
            return Swap.make_message()
        else:
            return Noop.make_message()

    prompt = '> '
    return CompositeNode(location,
                         [
                             TextNode(Location(), prompt),
                             InputNode(Location(x=len(prompt)),
                                       on_key=handle,
                                       transformer=clear_on_enter),
                             list_todos(Location(y=2), model)
                         ])


def status(model):
    completed = [todo for todo in model.todos if todo.completed]
    return f'{len(completed)}/{len(model.todos)}'


def help_text(model):
    tab = "[tab] to toggle focus"
    if model.adding:
        return tab
    else:
        return tab + " | [d] to delete task | [c] to mark task complete"


def clear_on_enter(code, text):
    if code == RET or code == TAB:
        return ''
    else:
        return text


def toggle_menu(model):
    def intercepter(ch):
        if ch in 'dD':
            return Del
        elif ch in 'cC':
            return Toggle
        elif ch == TAB:
            return Swap
        else:
            return None
    return menu.Menu(render_todos(model.todos, prefix='', space=False),
                     model.menu,
                     intercept=intercepter)


Node = Union[TextNode, InputNode, CompositeNode]


def view(model: Model) -> Node:
    if model.adding:
        node = input_todo(Location(y=1), model)
    else:
        node = CompositeNode(Location(y=3), [toggle_menu(model)])

    return CompositeNode(Location(),
                         [
                             TextNode(Location(), 'Todo List:', style=Style(
                                 x_rel=ALIGN_CENTER
                             )),
                             node,
                             TextNode(Location(),
                                      help_text(model),
                                      style=Style(
                                          y_rel=ALIGN_RIGHT,
                                          style=HIGHLIGHT,
                                          fill=True
                                      )),
                             TextNode(Location(x=1),
                                      status(model),
                                      style=Style(
                                          x_rel=ALIGN_RIGHT,
                                          y_rel=ALIGN_RIGHT,
                                          style=HIGHLIGHT
                                      ))])


def main():
    run(model=initial_model,
        update=update,
        view=view)


if __name__ == '__main__':
    main()
