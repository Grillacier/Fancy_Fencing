import curses
from Scene import Scene

scene = Scene()
print(scene)

stdscr = curses.initscr() #determining terminal type
curses.noecho() #turning off automatic echoing of keys to the screen
curses.cbreak() #reacting to keys without pressing enter

# curses.addstr("***************")
# curses.nocbreak()
# curses.echo()
# curses.endwin()
