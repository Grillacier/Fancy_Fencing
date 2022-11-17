from Player import Player

class Scene:
    def __init__(self) -> None:
        opened = self.openScene("default.ffscene")
        if opened == 0:
            self.obstacle = "ඞ"
            self.scene = self.draw()
            self.p1 = Player("Reblochon")
            self.p2 = Player("Jeromine")
        elif opened == 1:
            print("Wrong file extension, couldn't initialize the stage")
        elif opened == 2:
            print("Wrong characters in file, couldn't initialize the stage")

    def openScene(self, sceneFile) -> int:
        if ".ffscene" in sceneFile:
            with open (sceneFile, "r") as f:
                scene = (f.readline()).strip()
            print(scene)
            if "1" not in scene or "2" not in scene or "_" not in scene:
                return 2
            self.sceneFile = scene
            return 0
        else:
            return 1

    #drawing the stage
    def draw(self) -> str:
        stage = ""
        for char in self.sceneFile:
            if char == 'x':
                stage += self.obstacle
            elif char == '1':
                stage += "bite"
            else:
                stage += char
        print("stage : ", stage)
        return stage

    # constructors
    def get_scene(self) -> str:
        return self.scene

    def set_scene(self, scene) -> None:
        self.scene = scene