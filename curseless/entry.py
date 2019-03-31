from .curseless import Curseless

from .display.screen import Display
from .display.stylerender import StyleTextRenderer
from .display.terminal import Terminal
from .display.inputmanager import InputManager

import curses
import asyncio
import signal

from concurrent.futures.thread import ThreadPoolExecutor


async def shutdown(signal, loop, input_manager, executor):
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [t.cancel() for t in tasks]
    input_manager.shutdown()
    executor.shutdown()
    asyncio.gather(*tasks)
    curses.endwin()
    loop.stop()


def run(model, update, view, subs=[]):
    """
    Main entry point for running a curseless application.

    User provides a model, update function, view, and possibly
    subscriptions.
    """
    def main(stdscr):
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor(max_workers=4) as executor:
            # use signals to handle threading and graceful shutdown of asyncio
            input_manager = InputManager.from_stdin(loop, executor)
            screen = StyleTextRenderer(
                Display.with_standard_attributes(stdscr)
            )
            display = Terminal(input_manager, screen)

            Curseless(model=model,
                      update=update,
                      view=view,
                      display=display,
                      subs=subs).run()

            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

            def create_task(s):
                asyncio.create_task(shutdown(s, loop, input_manager, executor))

            for s in signals:
                loop.add_signal_handler(s,
                                        lambda: create_task(s))

            loop.run_forever()
    curses.wrapper(main)
