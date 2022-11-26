from Player import Player

class Scene:
    def __init__(self) -> None:
        opened = self.openScene("default.ffscene")
        if opened == 0:
            self.obstacle = "ඞ"
            self.scene = self.drawScene()
            self.p1 = Player(True, "Reblochon", self.coord1)
            self.p2 = Player(False, "Jeromine", self.coord2)
            self.length = len(self.scene)
        elif opened == 1:
            print("Wrong file extension, couldn't initialize the stage")
        elif opened == 2:
            print("Wrong characters in file, couldn't initialize the stage")

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
            # getting the players and obstacles' positions
            obs = []
            for i in range(len(scene)):
                if scene[i] == "1":
                    self.coord1 = i
                if scene[i] == "2":
                    self.coord2 = i
                if scene[i] == "x":
                    # self.coordObs = i
                    obs.append(i)
            print("obstacles :", obs)
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
        if player == 1 and self.p2.x-self.p1.x > 5:
            self.p1.moveRight()
        elif player == 2 and self.length -2> self.p2.x:
            self.p2.moveRight()

    def moveLeft(self, player) -> None:
        if player == 1 and self.p1.x > 1:
            self.p1.moveLeft()
        elif player == 2 and self.p2.x-self.p1.x > 5:
            self.p2.moveLeft()

    def __str__(self) -> str:
        # players = self.drawPlayers()
        scene = self.drawScene()
        character = ""
        character += " "*(self.p1.x) + "o" 
        character += " "*(self.p2.x-(self.p1.x+1)) + "o\n"
        character += " "*(self.p1.x) + "|_/"
        character += " "*(self.p2.x-(self.p1.x+5)) + "\_|\n"
        for i in range(self.p1.height-3):
            character += " "*(self.p1.x) + "|"
            character += " "*(self.p2.x-(self.p1.x+1)) + "|\n"
        character += " "*(self.p1.x-1) + "/|"
        character += " "*(self.p2.x-(self.p1.x+1)) + "|\ \n"
        #return scene
        return character + scene

    # constructors
    def get_scene(self) -> str:
        return self.scene

    def set_scene(self, scene) -> None:
        self.scene = scene