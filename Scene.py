from Player import Player

class Scene:
    def __init__(self) -> None:
        opened = self.openScene("default.ffscene")
        if opened == 0:
            self.obstacle = "ඞ"
            self.scene = self.drawScene()
            self.p1 = Player(True, "Reblochon")
            self.p2 = Player(False, "Jeromine")
            self.coord1 = self.coords()[0]
            self.coord2 = self.coords()[1]
        elif opened == 1:
            print("Wrong file extension, couldn't initialize the stage")
        elif opened == 2:
            print("Wrong characters in file, couldn't initialize the stage")

    # opening the file containing the stage
    def openScene(self, sceneFile) -> int:
        if ".ffscene" in sceneFile:
            with open (sceneFile, "r") as f:
                scene = (f.readline()).strip()
            # print(scene)
            if "1" in scene and "2" in scene and "_" in scene: # checking if the scene has a floor and 2 players
                for char in scene:
                    if char != "1" and char != "2" and char != "_" and char != "x": # checking if there isn't other characters than the ones we want
                        return 2
            self.sceneFile = scene
            return 0
        else:
            return 1

    # getting the players' positions
    def coords(self) -> tuple:
        x = 0
        y = 0
        for i in range(len(self.scene)):
            if str(i)== "1":
                x = i
            elif str(i) == "2":
                y = i
        return (x,y)

    # drawing the players
    def drawPlayers(self) -> str:
        players = ""
        for i in range(len(self.sceneFile)):
            if i == self.coord1:
                players += self.p1.drawPlayer()
            elif i == self.coord2:
                players += self.p2.drawPlayer()
            else:
                players += " "
        players += "\n"
        return players
            

    # drawing the scene with obstacles
    def drawScene(self) -> str:
        stage = ""
        for i in range(len(self.sceneFile)):
            if self.sceneFile[i] == "x":
                stage += self.obstacle
            else:
                stage += "_"
        return stage

    def __str__(self) -> str:
        players = self.drawPlayers()
        scene = self.drawScene()
        return players + scene

    # constructors
    def get_scene(self) -> str:
        return self.scene

    def set_scene(self, scene) -> None:
        self.scene = scene