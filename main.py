#!/usr/bin/env python3
import curses
from Scene import Scene


scene = Scene()

screen = curses.initscr()

# Update the buffer, adding text at different locations

curses.cbreak()
screen.keypad(1)
num_rows, num_cols = screen.getmaxyx()
screen.addstr(int(num_rows / 2),0, str(scene))
screen.addstr(int(num_rows / 2)+4,2, "p")
screen.refresh()

key = ''
while key != ord('m'):
    key = screen.getch()
    screen.addch(20,25,key)
    screen.refresh()
    if chr(key) == 'd': 
        scene.moveRight(1)
    elif chr(key) == 'q': 
        scene.moveLeft(1)
    elif key == curses.KEY_RIGHT:
        scene.moveRight(2)
    elif key == curses.KEY_LEFT: 
        scene.moveLeft(2)
    screen.addstr(int(num_rows / 2), 0, str(scene))
    screen.addstr(int(num_rows / 2)+4,2, "p")
    screen.refresh()
curses.endwin()


# Changes go in to the screen buffer and only get
# displayed after calling `refresh()` to update
screen.refresh()

curses.napms(3000)
curses.endwin()
#stdscr = curses.initscr() #determining terminal type
#curses.noecho() #turning off automatic echoing of keys to the screen
#curses.cbreak() #reacting to keys without pressing enter

# curses.addstr("***************")
# curses.nocbreak()
# curses.echo()
# curses.endwin()