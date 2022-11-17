class Player:
    def __init__(self, name = "Player") -> None:
        self.name = name
        self.height = 10
        self.score = 0

    def __str__(self) -> str:
        character = "o"
    