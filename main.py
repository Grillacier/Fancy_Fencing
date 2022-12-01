import curses
import threading
import time
from Scene import Scene
from Configuration import Configuration

config = Configuration()
# asks the user if they want to play on the default scene
c = input("Do you want to play with the default scene? (y/n) ")
if c[0].lower() == "y":
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
            file_scene = d[int(input("Choose the number of the scene you want to play on: "))] 
            print(file_scene)
            break
        except :
            print("Please choose a valid number") # asks again until a valid number is chosen        

c = input("Do you want to play with the default parameters? (y/n) ") # asks the user if they want to play with the default parameters
if(c[0].lower() == 'n'):
    param = config.choiceParam()
    scene = Scene(file = file_scene)
    scene.setParam(param[0], param[1], param[2], param[3], param[4], param[5], param[6], param[7], param[8], param[9], param[10], param[11], param[12])
else:
    scene = Scene(file = file_scene)
    scene.setParam(30, "Nathy", 2, 3, 4, 4, 60, "Ricky", 1, 4, 2, 3, 60) # Nathy and Ricky are my rabbits

curses.noecho() # pressed keys won't be printed on the screen
curses.cbreak() # reacting to keys without pressing enter

# t1 and t2 manage players' movements
t1 = threading.Thread(target=scene.moving, args=(1,)) # args should be a tuple
t2 = threading.Thread(target=scene.moving, args=(2,))
t3 = threading.Thread(target=scene.readKey , args=())

num_rows, num_cols = scene.screen.getmaxyx()

t1.start()
t2.start()
t3.start()

i = 0
while(scene.finish != 3):
    if scene.p1.score == scene.winningScore:
        scene.screen.clear()
        scene.screen.addstr(0, scene.length//2, scene.p1.name + " wins! Congratulations!")
        scene.screen.refresh()
        while scene.finish != 3:
            continue

    elif scene.p2.score == scene.winningScore:
        scene.screen.clear()
        scene.screen.addstr(0, scene.length//2, scene.p2.name + " wins! Congratulations!")
        scene.screen.refresh()
        while scene.finish != 3:
            continue

# main thread updating game's display
    scene.verrou.acquire()
    scene.screen.clear()
    scene.screen.addstr(0, scene.length//2-3, str(scene.p1.score) + " | " + str(scene.p2.score)) # score
    scene.screen.addstr(int(num_rows / 2), 0, str(scene)) # floor
    scene.addObstacles(int(num_rows)) # obstacles
    scene.add_player_scene(1, num_rows) # 1st player
    scene.add_player_scene(2, num_rows) # 2nd player
    if scene.pause :
        scene.screen.addstr(0, 0, "Pause\nPlayer 1 : Move left = q, Move right = d, Jump left = a, Jump right = e, Attack = z, Block = s\n" \
        "Player 2 : Move left = left arrow, Move right = right arrow, Jump left = l, Jump right = m, Attack = o, Block = p\nQuit = x ")
    
    scene.screen.refresh()
    scene.verrou.release()
    time.sleep(1/scene.frames_per_second)
    
curses.nocbreak()
scene.screen.keypad(False)
curses.endwin() # returns to normal terminal
