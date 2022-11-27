import curses

class Player:
    def __init__(self, player, name = "Player", x = 0 , y = 0 ) -> None:
        self.name = name
        self.height = 5
        self.player = player
        self.score = 0
        self.x = x
        self.y = y
        self.attack = False
        self.block = False
        self.rest = True
        self.attacking_speed = 1
        self.attacking_range = 1
        self.mouvement_speed = 1

    def drawPlayer(self) -> str:
        character = ""
        character += "o\n" 
        if self.player == 1:
            character += "|_/\n"
        else:
            character +=  "\_|\n"
        for i in range(self.height-3):
            character += "|\n"
        if self.player == 1:    
            character += "/|\n"
        else:
            character += "|\ \n"
        return character

    def moveRight(self) -> None:
        self.x += 1
    
    def moveLeft(self) -> None:
        self.x -= 1

    def pjumpRight(self) -> None:
        self.x += 1
        self.y += 1

    def pjump(self) -> None:
        self.y = 1
        
    def pdown(self) -> None:
        self.y = 0
    def __str__(self) -> str:
        return self.drawPlayer()
    
    # constructors
    def getX(self) -> int:
        return self.x

    def setX(self, x) -> None:
        self.x = x
    
    def getY(self) -> int:
        return self.y

    def setY(self, y) -> None:
        self.y = y

    