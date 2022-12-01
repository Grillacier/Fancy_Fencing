from Player import Player
import threading
import curses
import time

class Scene:
    verrou = threading.Lock()
      
    def __init__(self, frames_per_second=30, file="default.ffscene") -> None:
        opened = self.openScene(file)
        if opened == 0:
            self.screen = curses.initscr() # determining terminal type
            self.obstacle = "ඞ" # Among Us ඞ
            self.scene = self.drawScene()
            self.p1 = Player(1, "Nathy", self.coord1)
            self.p2 = Player(2, "Ricky", self.coord2)
            self.length = len(self.scene)
            self.frames_per_second = frames_per_second
            self.screen.keypad(True) # recognizing special characters
            self.eventPlayer1 = threading.Event()
            self.eventPlayer2 = threading.Event()
            self.keyPlayer1 = 0
            self.keyPlayer2 = 0
            self.winningScore = 3
            # player 1 lands on wall[0] after jumping, player 2 lands on wall[1] 
            # if a player doesn't jump, the value is -1
            self.wall = [-1, -1]
            self.pause = False
            self.finish = 0
            
        else: 
            if opened == 1:
                Scene.screen.addstr("Wrong file extension, couldn't initialize the stage")
            elif opened == 2:
                Scene.screen.addstr("Wrong characters in file, couldn't initialize the stage")
            elif opened == 3:
                Scene.screen.addstr("Player 2 can't be before Player 1, couldn't initialize the stage")
            elif opened == 4:
                Scene.screen.addstr("There should at least be '1', '2' and '_' in the file, couldn't initialize the stage")
   
    # opening the file containing the stage
    def openScene(self, sceneFile) -> int:
        if ".ffscene" in sceneFile:
            with open (sceneFile, "r") as f:
                scene = (f.readline()).strip()
            if "1" in scene and "2" in scene and "_" in scene:
                for char in scene:
                    if char != "1" and char != "2" and char != "_" and char != "x":
                        return 2 # there is at least one incorrect character
                self.sceneFile = scene
            else:
                return 4 # characters are missing

            # getting the players and obstacles' positions
            obs = []
            for i in range(len(scene)):
                if scene[i] == "1":
                    self.coord1 = i
                if scene[i] == "2":
                    self.coord2 = i
                if scene[i] == "x":
                    obs.append(i)

            if self.coord1 > self.coord2:
                return 3 # player 2 is before player 1
                
            self.coordObs = obs
            return 0 # no problem
            
        else:
            return 1 # wrong file extension
           
    # drawing the scene
    def drawScene(self) -> str:
        stage = ""
        for i in self.sceneFile:
            stage += "#"
        return stage
    

    '''movements'''
    def moveLeft(self, player) -> None:
        if player == 1:
            time.sleep(self.p1.movement_speed/self.frames_per_second)
        elif player == 2 :
            time.sleep(self.p2.movement_speed/self.frames_per_second)
        self.verrou.acquire()
        if player == 1 and self.p1.getX() > 0 and not self.leftObstacle(self.p1) :
            self.p1.pMoveLeft()
        elif player == 2 and self.p2.getX()-self.p1.getX() > 5 and not self.leftObstacle(self.p2) and self.wall[0] != self.p2.getX()-5:
            self.p2.pMoveLeft()
        self.verrou.release()

    def moveRight(self, player) -> None:
        if player == 1:
            time.sleep(self.p1.movement_speed/self.frames_per_second)
        elif player == 2 :
            time.sleep(self.p2.movement_speed/self.frames_per_second)
        self.verrou.acquire()
        if player == 1 and self.p2.getX()-self.p1.getX() > 5 and not self.rightObstacle(self.p1) and self.wall[1] != self.p1.getX()+5:
            self.p1.pMoveRight()
        elif player == 2 and self.length-1 > self.p2.getX() and not self.rightObstacle(self.p2):
            self.p2.pMoveRight()
        self.verrou.release()

    # returns True if there is an obstacle to the left of the player
    def leftObstacle(self, player) -> bool:
        for i in self.coordObs:
            if i == player.getX()-1:
                return True 
        return False

    # returns True if there is an obstacle to the right of the player
    def rightObstacle(self, player) -> bool:
        for i in self.coordObs:
            if i == player.getX()+1:
                return True
        return False

    # returns True if the character can jump to the left
    def canJumpL(self, player) -> bool:
        if player == 1:
            # if the player lands outside of the scene
            if self.p1.getX()-2 < 0:
                return False
            # if the player lands too close to the other player
            if self.p2.getX()-(self.p1.getX()-2) < 5:
                return False
            # if the player lands on an obstacle
            for i in self.coordObs:
                if i == self.p1.getX()-2:
                    return False

        elif player == 2:
            if self.p2.getX()-2 < 0:
                return False
            if (self.p2.getX()-2)-self.p1.getX() < 5:
                return False
            for i in self.coordObs:
                if i == self.p2.getX()-2:
                    return False

        return True

    # returns True if the character can jump to the right
    def canJumpR(self, player) -> bool:
        if player == 1:
            if self.p1.getX()+2 >= self.length:
                return False
            if self.p2.getX()-(self.p1.getX()+2) < 5:
                return False
            for i in self.coordObs:
                if i == self.p1.getX()+2:
                    return False

        elif player == 2:
            if self.p2.getX()+2 >= self.length:
                return False
            if (self.p2.getX()+2)-self.p1.getX() < 5:
                return False
            for i in self.coordObs:
                if i == self.p2.getX()+2:
                    return False

        return True

    def jumpLeft(self, player) -> None:
        t = 0
        if self.canJumpL(player):
            if player == 1:
                self.wall[0] = self.p1.getX()-2
                t = self.p1.movement_speed/self.frames_per_second
                time.sleep(t)
                self.p1.pJump()
                time.sleep(t)
                self.p1.pMoveLeft()
                self.p1.pMoveLeft()
                time.sleep(t)
                self.p1.pDown()
                self.wall[0] = -1

            elif player == 2 :
                self.wall[1] = self.p2.getX()-2
                t = self.p2.movement_speed/self.frames_per_second
                time.sleep(t)
                self.p2.pJump()
                time.sleep(t)
                self.p2.pMoveLeft()
                self.p2.pMoveLeft()
                time.sleep(t)
                self.p2.pDown()
                self.wall[1] = -1

    def jumpRight(self, player) -> None:
        t = 0
        if self.canJumpR(player):
            if player == 1:
                self.wall[0] = self.p1.getX()+2
                t = self.p1.movement_speed/self.frames_per_second
                time.sleep(t)
                self.p1.pJump()
                time.sleep(t)
                self.p1.pMoveRight()
                self.p1.pMoveRight()
                time.sleep(t)
                self.p1.pDown()
                self.wall[0] = -1

            elif player == 2 :
                self.wall[0] = self.p1.getX()+2
                t = self.p2.movement_speed/self.frames_per_second
                time.sleep(t)
                self.p2.pJump()
                time.sleep(t)
                self.p2.pMoveRight()
                self.p2.pMoveRight()
                time.sleep(t)
                self.p2.pDown()
                self.wall[1] = -1

    def attackSucceeds(self, player) -> bool:
        if player == 1:
            if self.p1.getState()[0] and (self.p2.getX()-self.p1.getX() <= self.p1.attacking_range+2):
                if (not self.p2.getState()[1]):
                    return True
                else:
                    return self.p1.attacking_range > self.p2.defending_range
                
        elif player == 2:
            if self.p2.getState()[0] and (self.p2.getX()-self.p1.getX() <= self.p2.attacking_range+2):
                if (not self.p1.getState()[1]):
                    return True
                else:
                    return self.p2.attacking_range > self.p1.defending_range

    def attack(self, player) -> None:
        if player == 1:
            time.sleep(self.p1.attacking_speed/self.frames_per_second)
            self.p1.pAttack()
            if (self.attackSucceeds(1) and self.attackSucceeds(2)) or self.isBlocked(2):
                self.p1.setX(self.coord1)
                self.p2.setX(self.coord2)
            elif self.attackSucceeds(1):
                self.p1.score+=1
                self.p1.setX(self.coord1)
                self.p2.setX(self.coord2)
            time.sleep(0.5)
            self.p1.pRest()

        elif player == 2:
            time.sleep(self.p2.attacking_speed/self.frames_per_second)
            self.p2.pAttack()
            if (self.attackSucceeds(1) and self.attackSucceeds(2)) or self.isBlocked(1):
                self.p1.setX(self.coord1)
                self.p2.setX(self.coord2)
            elif self.attackSucceeds(2):
                self.p2.score+=1
                self.p1.setX(self.coord1)
                self.p2.setX(self.coord2)
            time.sleep(0.5)
            self.p2.pRest()

    def isBlocked(self, player) -> bool:
        if player == 1:
            return self.p1.getState()[1] and self.p2.getState()[0] and self.p1.defending_range >= self.p2.attacking_range
        if player == 2:
            return self.p2.getState()[1] and self.p1.getState()[0] and self.p2.defending_range >= self.p1.attacking_range
    
    def block(self, player) -> None:
        if player == 1:
            self.p1.pBlock()
            time.sleep(self.p1.blocking_time/self.frames_per_second)
            self.p1.pRest()

        if player == 2:
            self.p2.pBlock()
            time.sleep(self.p2.blocking_time/self.frames_per_second)
            self.p2.pRest()

    def moving(self, player) -> None:  
        # if player == 1, the variables are the first values
        left, right, jumpL, jumpR, attack, block, event, key = (ord('q'), ord('d'), ord('a'), ord('e'), ord('z'), ord('s'), self.eventPlayer1, self.keyPlayer1)  if player == 1 \
        else (curses.KEY_LEFT, curses.KEY_RIGHT, ord('l'), ord('m'), ord('o'), ord('p'), self.eventPlayer2, self.keyPlayer2)  # if not, they are these values
        while True:  
            event.wait() # thread corresponding to the player waits to be woken up
            key = self.keyPlayer1 if player == 1 else self.keyPlayer2
            if key == right: 
                self.moveRight(player)   
            elif key == left: 
                self.moveLeft(player)
            elif key == jumpR: 
                self.jumpRight(player)
            elif key == jumpL: 
                self.jumpLeft(player)
            elif key == attack:
                self.attack(player)
            elif key == block:
                self.block(player)
            elif key == ord('x'):
                self.verrou.acquire()
                self.finish += 1
                self.verrou.release()
                return # function and player thread stop
            event.clear() # internal flag is set to False

    def __str__(self) -> str:
        scene = self.drawScene()
        return scene

    # prints the obstacles
    def addObstacles(self, num_rows) -> None:
        for i in self.coordObs:
            self.screen.addstr(int(num_rows / 2 - 1), i, self.obstacle)

    # prints the players
    def add_player_scene(self, player, num_rows) -> None:
        if player == 1:
            self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 1, self.p1.getX(), "o")
            if self.p1.getState()[0]:
                sword = min(self.p1.attacking_range, self.p2.getX()-self.p1.getX()+1) * "_"
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 2, self.p1.getX(), "|"+sword)
            elif self.p1.getState()[1]:
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 2, self.p1.getX(), "|_|")
            elif self.p1.getState()[2]:
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 2, self.p1.getX(), "|_/")
            for i in range(self.p1.height-3):
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + i + 3, self.p1.getX(), "|")
        
        elif player == 2:
            self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.getY() + 1, self.p2.getX(), "o")
            if self.p2.getState()[0]:
                sword = min(self.p2.attacking_range, self.p2.getX()-self.p1.getX()+1) * "_"
                self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.getY() + 2, self.p2.getX()-len(sword), sword+"|")
                if self.p1.getState()[2]:
                    self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 2, self.p1.getX(), "|_/")
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.getY() + 2, self.p1.getX(), "|")
            elif self.p2.getState()[1]:
                self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.getY() + 2, self.p2.getX()-2, "|_|")
            elif self.p2.getState()[2]:
                self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.getY() + 2, self.p2.getX()-2, "\_|")
            for i in range(self.p2.height-3):
                self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.getY() + i + 3, self.p2.getX(), "|")
            
    # returns true if key is one of player 1's keys
    def isKeyPlayer1(self, key) -> bool:
        return key == ord('q') or key == ord('d') or key == ord('a') or key == ord('e') or key == ord('z') or key == ord('s')
    
    # returns true if key is one of player 2's keys
    def isKeyPlayer2(self, key) -> bool:
        return key == curses.KEY_LEFT or key == curses.KEY_RIGHT or key == ord('m') or key == ord('l') or key == ord('o') or key == ord('p')

    # reads pressed keys and wakes the corresponding player thread up
    def readKey(self) -> None:
        key = ""
        while True:
            key = self.screen.getch() # gets pressed key
            if self.win() :
                key = ord('x')
                self.verrou.acquire()
                self.finish += 1
                self.verrou.release()
                self.keyPlayer1 = key
                self.eventPlayer1.set() # wakes the thread up, internal flag is set to True
                self.keyPlayer2 = key
                self.eventPlayer2.set()
                return
                
            if key == ord('n'): # pause
                self.pause = True
                key = ""
                while key != ord('n'):
                    key = self.screen.getch()
                    if key == ord('x'):
                        self.verrou.acquire()
                        self.finish += 1
                        self.verrou.release()
                        self.keyPlayer1 = key
                        self.eventPlayer1.set() # wakes the thread up, internal flag is set to True
                        self.keyPlayer2 = key
                        self.eventPlayer2.set()
                        return
                self.pause = False

            if self.isKeyPlayer1(key):
                self.keyPlayer1 = key
                self.eventPlayer1.set()

            elif self.isKeyPlayer2(key):
                self.keyPlayer2 = key
                self.eventPlayer2.set()
                
    # setting players' parameters
    def setParam(self,fps, player_name1, movement_speed_player1, attacking_range_player1, attacking_speed_player1, defending_range_player1, blocking_time_player1, 
                player_name2, movement_speed_player2, attacking_range_player2, attacking_speed_player2, defending_range_player2, blocking_time_player2):
        self.frames_per_second = abs(fps)
        self.p1.name = player_name1
        self.p1.movement_speed = abs(movement_speed_player1)
        self.p1.attacking_range = abs(attacking_range_player1)
        self.p1.attacking_speed = abs(attacking_speed_player1)
        self.p1.defending_range = abs(defending_range_player1)
        self.p1.blocking_time = abs(blocking_time_player1)
        self.p2.name = player_name2
        self.p2.movement_speed = abs(movement_speed_player2)
        self.p2.attacking_range = abs(attacking_range_player2)
        self.p2.attacking_speed = abs(attacking_speed_player2)
        self.p2.defending_range = abs(defending_range_player2)
        self.p2.blocking_time = abs(blocking_time_player2)

    def win(self) -> bool:
        return self.p1.score == self.winningScore or self.p2.score == self.winningScore