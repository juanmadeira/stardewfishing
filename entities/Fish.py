import random
from lib import graphics as gph
from entities import Entity

class Fish(Entity):
    def __init__(self, sprite: gph.Image, window: gph.GraphWin, game):
        super().__init__(sprite, window)
        self.game = game
        self.lastHorizontalFlick = 2

    def horizontalFlick(self):
        self.sprite.move(self.lastHorizontalFlick, 0)
        self.lastHorizontalFlick *= -1

    def getDifficulty(self):
        return random.choices(
            ["easy", "medium", "hard"],
            weights=[0.45, 0.35, 0.2],
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
                weights=[0.05, 0.25, 0.7],
                k=1
            )[0]
        return False
    
    def getFishSpecie(self, rarity):
        fishes = self.game.assets/"fishes"/rarity
        files = list(fishes.glob("*.png"))
        return random.choice(files).stem