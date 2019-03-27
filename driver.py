import curses

from curseless.display.styles import RED
from curseless.display.screen import Display
from curseless.location import Location

from time import sleep


def main(stdscr):
    display = Display.with_standard_attributes(stdscr)
    display.update(Location(), '', 'Test text', style=RED)
    display.draw(Location())
    while True:
        sleep(1)


if __name__ == '__main__':
    curses.wrapper(main)
