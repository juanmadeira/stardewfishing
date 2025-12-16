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

    def randomizeMovement(self):
        return random.choices([-1,0,1], [0.30, 0.1, 0.30])[0]

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
        
        if difficulty == "medium":
            return random.choices(
                ["common", "uncommon", "rare"],
                weights=[0.35, 0.5, 0.15],
                k=1
            )[0]
        
        if difficulty == "hard":
            return random.choices(
                ["common", "uncommon", "rare"],
                weights=[0.2, 0.5, 0.3],
                k=1
            )[0]
        
        return False
    
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