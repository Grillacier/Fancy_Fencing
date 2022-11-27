#!/usr/bin/env python3
import curses
from Scene import Scene
import Player
import threading
import time

scene = Scene()
curses.noecho()
#threads des déplacements des joueurs (t1 et t2)
t1 = threading.Thread(target=scene.moving, args=(1,))
t2 = threading.Thread(target=scene.moving, args=(2,))
t3 = threading.Thread(target=scene.readKey , args=()) #readKey pour réveiller bon thread
num_rows, num_cols = scene.screen.getmaxyx()
scene.screen.addstr(int(num_rows / 2), 0, str(scene))
scene.addObstacles(int(num_rows))
scene.add_player_scene(1, num_rows)
scene.add_player_scene(2, num_rows)
t1.start()
t2.start()
t3.start()

i = 0
while(True):
# thread principal pour màj affichage
    scene.verrou.acquire()
    scene.screen.clear()
    scene.screen.addstr(int(num_rows / 2), 0, str(scene))
    scene.addObstacles(int(num_rows))
    scene.add_player_scene(1, num_rows)
    scene.add_player_scene(2, num_rows)
    scene.screen.refresh()
    scene.verrou.release()
    #TODO: remplacer 30 par nombre fps entré en argumentd
    time.sleep(1/30)
    


# # Changes go in to the screen buffer and only get
# # displayed after calling `refresh()` to update

# #stdscr = curses.initscr() #determining terminal type
# #curses.noecho() #turning off automatic echoing of keys to the screen
# #curses.cbreak() #reacting to keys without pressing enter

# # curses.addstr("***************")
curses.endwin()
