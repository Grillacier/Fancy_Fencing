import os

class Configuration:
    # list all the scenes in the scene directory
    def list_scenes(self):
        scenes = dict()
        for file in os.listdir("scenes"):
            with open("scenes/" + file, "r") as f:
                scenes["scenes/" + file] = f.readline()
        return scenes

    # asks the user to choose the parameters for the game
    def choiceParam(self):
        try: 
            fps = int(input("Choose the number of frames per second: "))
            player_name1 = input("Choose the name of player 1: ")
            movement_speed_player1 = int(input("Choose the movement speed of player 1: "))
            attacking_range_player1 = int(input("Choose the attacking range of player 1: "))
            attacking_speed_player1 = int(input("Choose the attacking speed of player 1: "))
            defending_range_player1 = int(input("Choose the defending range of player 1: "))
            blocking_time_player1 = int(input("Choose the blocking time of player 1: "))
            player_name2 = input("Choose the name of player 2: ")
            movement_speed_player2 = int(input("Choose the movement speed of player 2: "))
            attacking_range_player2 = int(input("Choose the attacking range of player 2: "))
            attacking_speed_player2 = int(input("Choose the attacking speed of the player 2: "))
            defending_range_player2 = int(input("Choose the defending range of player 2: "))
            blocking_time_player2 = int(input("Choose the blocking time of player 2: "))
            return (fps, player_name1, movement_speed_player1, attacking_range_player1, attacking_speed_player1, defending_range_player1, blocking_time_player1,
            player_name2, movement_speed_player2, attacking_range_player2, attacking_speed_player2, defending_range_player2, blocking_time_player2)
        
        except ValueError:
            print("Please choose a number")
            exit() # no second chance if the wrong value is entered because I'm too lazy