Curseless
---------
Provides a simple framework for making interactive terminal apps.

The approach is based off of the Elm architecture.

The view is declared using provided elements:
```python
TextNode(Location(),
         "Hello World",
         style=Style(
             x_rel=ALIGN_RIGHT,
             y_rel=ALIGN_RIGHT,
             style=HIGHLIGHT
         ))
```
This would render "Hello World" (highlighted) in the bottom-right corner of the terminal.

Each time the view updates, the library (naively) figures out what has changed and what needs to be deleted and renderered.


## Requirements:
- Uses asyncio (Python3, version 3.5+)
- Curses (A Python library for buidling things on the command line)

## Linting:
* run `flake8` within the project directory

## Testing:
To run the tests, run `nosetests` from within the project directory

## Running samples:
-  `python -m samples.todo.main`

### See the sample folder to get an idea of the different kinds of things we can build with this:

#### Hangman:
![Alt Text](https://media.giphy.com/media/9MImSv2R1y00kuIZki/giphy.gif)

#### Brainstorming:
![Alt Text](https://media.giphy.com/media/APbupIbKZvDxY1WxsS/giphy.gif)

#### Canonical Todo List:
![Alt Text](https://media.giphy.com/media/4H94dEiVGEIvzfXNqF/giphy.gif)


#### Some Example Code:
Most files will provide 3 functions:
1. Model - a global state (should be immutable)
```python
class Todo(NamedTuple):
    task: str 
    completed: bool = False


class Model(NamedTuple):
    todos: List[Todo]
```
Note that using MyPy typing is optional but potentially helpful
\
\
\
2. Update - a function that is passed the current model state and a message
Message constrution helper:
```python
Toggle = Message[int]('TOGGLE')
```

Snippet of relevant code that updates the model:
```python
index = Toggle.retrieve_payload(msg)
todos = [todo if i != index else Todo(task=todo.task,
                                      completed=not todo.completed)
         for i, todo in enumerate(model.todos)]
return model._replace(todos=todos)
```
\
\
3. View - Takes in the model and renders to the terminal

Portion that renders the items:
```python
def render_todo(i, todo, prefix):
    if todo.completed:
        style = Style(style=[GREEN, DIM])
    else:
        style = Style(style=DEFAULT)
    return TextNode(Location(y=i), prefix + todo.task, style=style)


def render_todos(todos, prefix):
    return [render_todo(i, todo, prefix) for i, todo in enumerate(todos)]


def list_todos(location, model, prefix='- '):
    return CompositeNode(location, render_todos(model.todos, prefix))
```
