import random
from lib import graphics as gph
from entities import Entity

class Fish(Entity):
    def __init__(self, sprite: gph.Image, window: gph.GraphWin):
        super().__init__(sprite, window)
        self.lastHorizontalFlick = 2

    def horizontalFlick(self):
        self.sprite.move(self.lastHorizontalFlick, 0)
        self.lastHorizontalFlick *= -1

    def getDifficulty(self):
        return random.choices(
            ["easy", "medium", "hard"],
            weights=[0.5, 0.3, 0.2],
            k=1
        )[0]
    
    def getRarity(self, difficulty):
        if difficulty == "easy":
            return random.choices(
                ["common", "uncommon", "rare"],
                weights=[0.7, 0.25, 0.05],
                k=1
            )[0]
        elif difficulty == "medium":
            return random.choices(
                ["common", "uncommon", "rare"],
                weights=[0.35, 0.5, 0.15],
                k=1
            )[0]
        elif difficulty == "hard":
            return random.choices(
                ["common", "uncommon", "rare"],
                weights=[0.2, 0.5, 0.3],
                k=1
            )[0]
        return False