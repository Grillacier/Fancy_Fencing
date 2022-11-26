class Player:
    def __init__(self, first, name = "Player", x = 0 , y = 0) -> None:
        self.first = first
        self.name = name
        self.height = 5
        self.first = first
        self.score = 0
        self.x = x
        self.y = y

    def head(self) -> str:
        if self.first:
            return "(╬ಠ益ಠ)"
        else:
            return "(–︿–ꐦ)"

    def arms(self) -> str:
        if self.first:
            return "   |_/"
        else:
            return " \_|  "

    def body(self) -> str:
        return "   |   "

    def feet(self) -> str:
        if self.first:
            return "  /|  "
        else:
            return "   |\ "

    def drawPlayer(self) -> str:
        character = self.head() + "\n" + self.arms() + "\n"
        for i in range(self.height-3):
            character += self.body() + "\n"
        character += self.feet()
        return character

    def drawPlayer(self) -> str:
        character = ""
        if self.first:
            character += "(╬ಠ益ಠ)\n"
            character += "   |_/\n"
        else:
            character += "(–︿–ꐦ)\n"
            character += " \_|  \n"
        for i in range(self.height-3):
            character += "   |   \n"
        if self.first:
            character += "  /|  "
        else:
            character += "   |\ "
        return character

    def moveRight(self) -> None:
        self.x += 1
    
    def moveLeft(self) -> None:
        self.x -= 1
        
    def __str__(self) -> str:
        return self.drawPlayer()