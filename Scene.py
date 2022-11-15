from Player import Player

class Scene:
    def __init__(self) -> None:
        self.obstacle = "ඞ"
        self.scene = self.draw("default.ffscene")
        self.p1 = Player("Reblochon")
        self.p2 = Player("Jeromine")

    #getting the stage
    def draw(self, sceneFile) -> str:
        with open (sceneFile, "r") as f:
            scene = (f.readline()).strip()
        
        print(scene)
        stage = ""
        for char in scene:
            if char == 'x':
                stage += self.obstacle
            elif char == 1:
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