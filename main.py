#!/usr/bin/env python3
import curses
from Scene import Scene
import Player
import threading
import time
import math
import os

# Liste tous les fichiers (scenes) dans le répertoir scenes
def list_scenes():
    scenes = dict()
    for file in os.listdir("scenes"):
        with open("scenes/"+file, "r") as f:
            scenes["scenes/"+file] = f.readline()
    return scenes

# Demande à l'utilisateur de choisir les paramètres de la partie
def choiceParam():
    try: 
        fps = int(input("Enter the number of frames per second: "))
        player_name1 = input("Enter the name of the player 1: ")
        mouvement_speed_player1 = int(input("Enter the mouvement speed of the player 1: "))
        attacking_range_player1 = int(input("Enter the attacking range of the player 1: "))
        attacking_speed_player1 = int(input("Enter the attacking speed of the player 1: "))
        blocking_time_player1 = int(input("Enter the blocking time of the player 1: "))
        player_name2 = input("Enter the name of the player 2: ")
        mouvement_speed_player2 = int(input("Enter the mouvement speed of the player 2: "))
        attacking_range_player2 = int(input("Enter the attacking range of the player 2: "))
        attacking_speed_player2 = int(input("Enter the attacking speed of the playedr 2: "))
        blocking_time_player2 = int(input("Enter the blocking time of the player 2: "))
        return (fps, player_name1, mouvement_speed_player1, attacking_range_player1, attacking_speed_player1, blocking_time_player1,
         player_name2, mouvement_speed_player2, attacking_range_player2, attacking_speed_player2, blocking_time_player2)
    except ValueError:
        print("Please enter a number")
        exit()

c = input("Do you want to play with the default scene? (y/n) ") # Demande à l'utilisateur s'il veut jouer avec la scène par défaut 
if c == "y":
       file_scene = "default.ffscene" # Si oui, on utilise la scène par défaut
else :
    scenes = list_scenes() # Sinon, on liste les scènes disponibles
    i = 1
    d = dict()
    for key, value in scenes.items():
        print(i, value)
        d[i] = key
        i += 1
    # On demande à l'utilisateur de choisir une scène parmi les scènes disponibles
    while True:
        try :
            file_scene = d[int(input("Enter the number of the scene you want to play: "))] 
            print(file_scene)
            break
        except :
            print("Please enter a valid number") # Si l'utilisateur entre un nombre invalide, on lui redemande de choisir une scène        

c = input("Do you want to play with the default parameters? (y/n) ") # Demande à l'utilisateur s'il veut jouer avec les paramètres par défaut
if(c=='n'):
    param = choiceParam()
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
# #curses.cbreak() #reacting to keys without pressing enter

# # curses.addstr("***************")
curses.endwin()
