import random as rd
from lib import gph, ASSETS_DIR
from entities import Entity

class Fish(Entity):
    def __init__(self, sprite: gph.Image, window: gph.GraphWin):
        super().__init__(sprite, window)
        self.lastHorizontalFlick = 2

    def horizontalFlick(self):
        self.sprite.move(self.lastHorizontalFlick, 0)
        self.lastHorizontalFlick *= -1

    def randomizeMovement(self, difficulty):
        if difficulty == "easy":
            return rd.choices([1,0,-1], [0.20, 0.60, 0.20])[0]
        if difficulty == "medium":
            return rd.choices([1,0,-1], [0.30, 0.40, 0.30])[0]
        if difficulty == "hard":
            return rd.choices([1,0,-1], [0.8, 0.1, 0.8])[0]
        return False

    def getDifficulty(self):
        return rd.choices(
            ["easy", "medium", "hard"],
            weights=[0.45, 0.35, 0.2],
            k=1
        )[0]
    
    def getRarity(self, difficulty):
        if difficulty == "easy":
            return rd.choices(
                ["common", "uncommon", "rare"],
                weights=[0.74, 0.25, 0.01],
                k=1
            )[0]
        
        if difficulty == "medium":
            return rd.choices(
                ["common", "uncommon", "rare"],
                weights=[0.3, 0.6, 0.1],
                k=1
            )[0]
        
        if difficulty == "hard":
            return rd.choices(
                ["uncommon", "rare"],
                weights=[0.20, 0.80],
                k=1
            )[0]
        return False
        
    def getRarityColor(self, rarity):
        return {
            "common": "green",
            "uncommon": "orange",
            "rare": "red",
        }[rarity]
    
    def getFishSpecie(self, rarity):
        fishes = ASSETS_DIR/"fishes"/rarity
        files = list(fishes.glob("*.png"))
        return rd.choice(files).stem
    
    def move(self, amount):
        new_y = self.getCenterY() - amount
        if new_y > self.getLowerLimit():
            new_y = self.getLowerLimit()
        elif new_y < self.getUpperLimit():
            new_y = self.getUpperLimit()
        self.sprite.move(0, new_y - self.getCenterY())

    def isAtBarLimit(self):
        if self.isAtUpperLimit() or self.isAtLowerLimit():
            return True
        return False
    
    def isAtUpperLimit(self):
        if self.getCenterY() <= self.getUpperLimit():
            return True
        return False
    
    def isAtLowerLimit(self):
        if self.getCenterY() >= self.getLowerLimit():
            return True
        return False

    def getLowerLimit(self):
        return 637 - self.height/2
    
    def getUpperLimit(self):
        return 74 + self.height/2