import curses
import threading
import time
from Scene import Scene
from Configuration import Configuration

config = Configuration()
# ask the user if they want to play on the default scene
c = input("Do you want to play with the default scene? (y/n) ")
if c == "y":
       file_scene = "default.ffscene"
else :
    scenes = config.list_scenes()
    i = 1
    d = dict()
    for key, value in scenes.items():
        print(i, "->", value)
        d[i] = key
        i += 1
    # the user chooses a scene among those existing
    while True:
        try :
            file_scene = d[int(input("Choose the number of the scene you want to play: "))] 
            print(file_scene)
            break
        except :
            print("Please Choose a valid number") # Si l'utilisateur entre un nombre invalide, on lui redemande de choisir une scène        

c = input("Do you want to play with the default parameters? (y/n) ") # Demande à l'utilisateur s'il veut jouer avec les paramètres par défaut
if(c=='n'):
    param = config.choiceParam()
    scene = Scene(file=file_scene)
    scene.setParam(param[0], param[1], param[2], param[3], param[4], param[5], param[6], param[7], param[8], param[9], param[10])
else:
    scene = Scene(file=file_scene)
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
while(scene.finish!=3):
# thread principal pour màj affichage
    scene.verrou.acquire()
    scene.screen.clear()
    scene.screen.addstr(int(num_rows / 2), 0, str(scene))
    scene.addObstacles(int(num_rows))
    scene.add_player_scene(1, num_rows)
    scene.add_player_scene(2, num_rows)
    if scene.pause :
        scene.screen.addstr(0, 0, "Pause\nPlayer 1 : Move left = q, Move right = d, Jump left = a, Jump right = e, Attack = z, Block = a\n" \
        "Player 2 : Move left = left arrow, Move right = right arrow, Jump left = l, Jump right = m, Attack = o, Block = p\nQuit = x ")
    scene.screen.refresh()
    scene.verrou.release()
    #TODO: remplacer 30 par nombre fps entré en argumentd
    time.sleep(1/scene.frames_per_second)
    


# # Changes go in to the screen buffer and only get
# # displayed after calling `refresh()` to update

# #stdscr = curses.initscr() #determining terminal type
# #curses.noecho() #turning off automatic echoing of keys to the screen
# #curses.cbreak() #reacting to keys without pressing Choose

# # curses.addstr("***************")
curses.endwin()
