from Player import Player
import threading
import curses
import time
class Scene:
    verrou = threading.Lock()
    screen = curses.initscr()
    
    def __init__(self, frames_per_second=30) -> None:
        opened = self.openScene("default.ffscene")
        if opened == 0:
            self.obstacle = "ඞ"
            self.scene = self.drawScene()
            self.p1 = Player(1, "Reblochon", self.coord1)
            self.p2 = Player(2, "Jeromine", self.coord2)
            self.length = len(self.scene)
            self.frames_per_second = frames_per_second
            self.screen.keypad(True)
            self.eventPlayer1 = threading.Event()
            self.eventPlayer2 = threading.Event()
            self.p1.mouvement_speed = 15
            self.keyPlayer1 = 0
            self.keyPlayer2 = 0
        else: 
            if opened == 1:
                Scene.screen.addstr("Wrong file extension, couldn't initialize the stage\n")
            elif opened == 2:
                Scene.screen.addstr("Wrong characters in file, couldn't initialize the stage\n")
            elif opened == 3:
                Scene.screen.addstr("Player 2 can't be before Player 1, couldn't initialize the stage\n")
            elif opened == 4:
                Scene.screen.addstr("There should only be '1', '2' and '_' in the file, couldn't initialize the stage\n")
            self.finalize()
   
    # constructors
    def getScene(self) -> str:
        return self.scene

    def setScene(self, scene) -> None:
        self.scene = scene

    # opening the file containing the stage
    def openScene(self, sceneFile) -> int:
        if ".ffscene" in sceneFile:
            with open (sceneFile, "r") as f:
                scene = (f.readline()).strip()
            if "1" in scene and "2" in scene and "_" in scene: # checking if the scene has a floor and 2 players
                for char in scene:
                    if char != "1" and char != "2" and char != "_" and char != "x": # checking if there isn't other characters than the ones we want
                        return 2
                self.sceneFile = scene
            else:
                return 4

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
                return 3
                
            self.coordObs = obs
            return 0
            
        else:
            return 1
           
    # drawing the scene with obstacles
    def drawScene(self) -> str:
        stage = ""
        for i in self.sceneFile:
            stage += "#"
        return stage
    

    def moveRight(self, player) -> None:
        if player == 1:
            time.sleep(self.p1.mouvement_speed/self.frames_per_second)
        elif player == 2 :
            time.sleep(self.p2.mouvement_speed/self.frames_per_second)
        self.verrou.acquire()
        if player == 1 and self.p2.x-self.p1.x > 5 and not self.rightObstacle(self.p1):
            self.p1.moveRight()
        elif player == 2 and self.length -2> self.p2.x and not self.rightObstacle(self.p2):
            self.p2.moveRight()
        self.verrou.release()

    def moveLeft(self, player) -> None:
        if player == 1:
            time.sleep(self.p1.mouvement_speed/self.frames_per_second)
        elif player == 2 :
            time.sleep(self.p2.mouvement_speed/self.frames_per_second)
        self.verrou.acquire()
        if player == 1 and self.p1.x > 0 and not self.leftObstacle(self.p1) :
            self.p1.moveLeft()
        elif player == 2 and self.p2.x-self.p1.x > 5 and not self.leftObstacle(self.p2):
            self.p2.moveLeft()
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
            # if the player lands on the other player
            if self.p1.x-2 == self.p2.x:
                return False
            # if the player lands on an obstacle
            for i in self.coordObs:
                if i == self.p1.x-2:
                    return False
            # if the player lands outside of the scene
            if self.p1.x-2 < 0:
                return False
            # if the player lands too close to the other player
            if abs(self.p2.x-(self.p1.x-2)) < 5:
                return False

        elif player == 2:
            if self.p2.x-2 == self.p1.x:
                return False
            for i in self.coordObs:
                if i == self.p2.x-2:
                    return False
            if self.p2.x-2 < 0:
                return False
            if abs((self.p2.x-2)-self.p1.x) < 5:
                return False


        return True

    # returns True if the character can jump to the right
    def canJumpR(self, player) -> bool:
        if player == 1:
            if self.p1.x+2 == self.p2.x:
                return False
            for i in self.coordObs:
                if i == self.p1.x+2:
                    return False
            if self.p1.x+2 >= self.length:
                return False
            if abs(self.p2.x-(self.p1.x+2)) < 5:
                return False

        elif player == 2:
            if self.p2.x+2 == self.p1.x:
                return False
            for i in self.coordObs:
                if i == self.p2.x+2:
                    return False
            if self.p2.x+2 >= self.length:
                return False
            if abs((self.p2.x+2)-self.p1.x) < 5:
                return False

        return True

    def jumpLeft(self, player) -> None:
        t = 0
        if self.canJumpL(player):
            if player == 1:
                t = self.p1.mouvement_speed/self.frames_per_second
                time.sleep(t)
                self.p1.pjump()
                time.sleep(t)
                self.p1.moveLeft()
                self.p1.moveLeft()
                time.sleep(t)
                self.p1.pdown()
            elif player == 2 :
                t = self.p2.mouvement_speed/self.frames_per_second
                time.sleep(t)
                self.p2.pjump()
                time.sleep(t)
                self.p2.moveLeft()
                self.p2.moveLeft()
                time.sleep(t)
                self.p2.pdown()

    def jumpRight(self, player) -> None:
        t = 0
        if self.canJumpR(player):
            if player == 1:
                t = self.p1.mouvement_speed/self.frames_per_second
                time.sleep(t)
                self.p1.pjump()
                time.sleep(t)
                self.p1.moveRight()
                self.p1.moveRight()
                time.sleep(t)
                self.p1.pdown()
            elif player == 2 :
                t = self.p2.mouvement_speed/self.frames_per_second
                time.sleep(t)
                self.p2.pjump()
                time.sleep(t)
                self.p2.moveRight()
                self.p2.moveRight()
                time.sleep(t)
                self.p2.pdown()

    def moving(self, player) -> None:  
        # if player == 1, affecte premières touche aux var
        # event dans thread : réveiller thread j1 ou j2
        left, right, jumpL, jumpR, event, key = (ord('q'), ord('d'), ord('a'), ord('e'), self.eventPlayer1, self.keyPlayer1)  if player == 1 \
        else (curses.KEY_LEFT, curses.KEY_RIGHT, ord('l'), ord('m'), self.eventPlayer2, self.keyPlayer2)  # sinon ces touches
        while key != ord('p'):  
            event.wait() # thread attend réveil
            print(player)
            key = self.keyPlayer1 if player == 1 else self.keyPlayer2
            if key == right: 
                self.moveRight(player)   
            elif key == left: 
                self.moveLeft(player)
            elif key == jumpR: 
                self.jumpRight(player)
            elif key == jumpL: 
                self.jumpLeft(player)
            event.clear()
        curses.endwin()

    def __str__(self) -> str:
        # players = self.drawPlayers()
        scene = self.drawScene()
        character = ""
        # if(self.p1.y==1 and self.p2.y==0):
        #     character += " "*(self.p1.x) + "o\n" 
        #     character += " "*(self.p1.x) + "|_/"
        #     character += " "*(self.p2.x-(self.p1.x+3)) + "o\n"
        #     character += " "*(self.p1.x) + "|"
        #     character += " "*(self.p2.x-(self.p1.x+3)) + "\_|\n"
        #     for i in range(self.p1.height-4):
        #         character += " "*(self.p1.x) + "|"
        #         character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        #     character += " "*(self.p1.x-1) + "/|"
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        #     character += " "*(self.p2.x) + "|\ \n"
        # elif self.p1.y==0 and self.p2.y==1:
        #     character += " "*(self.p2.x) + "o\n"
        #     character += " "*(self.p1.x) + "o" 
        #     character += " "*(self.p2.x-(self.p1.x+3)) + "\_|\n"
        #     character += " "*(self.p1.x) + "|_/"
        #     character += " "*(self.p2.x-(self.p1.x+3)) + "|\n"
            
        #     for i in range(self.p1.height-4):
        #         character += " "*(self.p1.x) + "|"
        #         character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        #     character += " "*(self.p1.x) + "|"
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "|\ \n"
        #     character += " "*(self.p1.x-1) + "/|\n"
        # elif self.p1.y==1 and self.p2.y==1:
        #     character += " "*(self.p1.x) + "o" 
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "o\n"
        #     character += " "*(self.p1.x) + "|_/"
        #     character += " "*(self.p2.x-(self.p1.x+5)) + "\_|\n"
        #     for i in range(self.p1.height-3):
        #         character += " "*(self.p1.x) + "|"
        #         character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        #     character += " "*(self.p1.x-1) + "/|"
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "|\ \n"
        #     character += "\n"
            
        # else:
        #     character += " "*(self.p1.x) + "o" 
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "o\n"
        #     character += " "*(self.p1.x) + "|_/"
        #     character += " "*(self.p2.x-(self.p1.x+5)) + "\_|\n"
        #     for i in range(self.p1.height-3):
        #         character += " "*(self.p1.x) + "|"
        #         character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        #     character += " "*(self.p1.x-1) + "/|"
        #     character += " "*(self.p2.x-(self.p1.x+1)) + "|\ \n"
        return character + scene

    def addObstacles(self, num_rows) -> None:
        for i in self.coordObs:
            self.screen.addstr(int(num_rows / 2 - 1), i, self.obstacle)

    def add_player_scene(self, player, num_rows) -> None:
        if player == 1:
            self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.y + 1, self.p1.x, "o")
            self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.y + 2, self.p1.x, "|_/")
            for i in range(self.p1.height-4):
                self.screen.addstr(int(num_rows / 2) - self.p1.height - self.p1.y + i + 3, self.p1.x, "|")
            self.screen.addstr(int(num_rows / 2)-1-self.p1.y, self.p1.x, "|")
        elif player == 2:
            self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.y + 1, self.p2.x, "o")
            self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.y + 2, self.p2.x-2, "\_|")
            for i in range(self.p2.height-4):
                self.screen.addstr(int(num_rows / 2) - self.p2.height - self.p2.y + i +3, self.p2.x, "|")
            self.screen.addstr(int(num_rows / 2) - 1 - self.p2.y, self.p2.x, "|")
            
    # Renvoie true si key correspond à une touche du joueur 1
    def isKeyPlayer1(self, key) -> bool:
        return key == ord('q') or key == ord('d') or key == ord('a') or key == ord('e')
    
    # Renvoie true si key correspond à une touche du joueur 2
    def isKeyPlayer2(self, key) -> bool():
        return key == curses.KEY_LEFT or key == curses.KEY_RIGHT or key == ord('m') or key == ord('l')

    # Lis les touches pressées et réveille le thread du joueur correspondant
    def readKey(self) -> None:
        key = ""
        while key != ord('p'):
            key = self.screen.getch() # lit touches pressées
            if self.isKeyPlayer1(key):
                self.keyPlayer1 = key
                self.eventPlayer1.set()
            elif self.isKeyPlayer2(key):
                self.keyPlayer2 = key
                self.eventPlayer2.set()