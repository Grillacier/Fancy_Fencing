class Player:
    def __init__(self, player, name = "Player", x = 0 , y = 0) -> None:
        self.name = name
        self.height = 5
        self.player = player
        self.score = 0
        self.x = x
        self.y = y
        self.attack = False
        self.block = False
        self.rest = True
        self.movement_speed = 1
        self.attacking_range = 3
        self.attacking_speed = 1
        self.defending_range = 2
        self.blocking_time = 60

    def pMoveRight(self) -> None:
        self.x += 1
    
    def pMoveLeft(self) -> None:
        self.x -= 1

    def pJump(self) -> None:
        self.y = 1
        
    def pDown(self) -> None:
        self.y = 0

    def pAttack(self) -> None:
        self.setState(True, False, False)

    def pBlock(self) -> None:
        self.setState(False, True, False)

    def pRest(self) -> None:
        self.setState(False, False, True)

    # constructors
    def getX(self) -> int:
        return self.x

    def setX(self, x) -> None:
        self.x = x
    
    def getY(self) -> int:
        return self.y

    def setY(self, y) -> None:
        self.y = y

    def getState(self) -> list:
        return [self.attack, self.block, self.rest]

    def setState(self, attack, block, rest) -> None:
        self.attack = attack
        self.block = block
        self.rest = rest