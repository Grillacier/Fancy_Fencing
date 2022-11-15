import curses #ne marche pas avec python3.10 sur windows
from Scene import Scene

scene = Scene()
scene.draw("default.ffscene")

#stdscr = curses.initscr()