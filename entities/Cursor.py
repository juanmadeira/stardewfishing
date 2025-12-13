from lib import graphics as gph
from entities import Entity

class Cursor(Entity):
    def __init__(self, difficulty, window: gph.GraphWin, game):
        self.game = game
        sprite = self.getSprites(difficulty)
        super().__init__(sprite, window)

    def getSprites(self, difficulty):
        if difficulty == "easy":
            return gph.Image(gph.Point(1060, 520), self.game.assets/"cursor-easy.png")
        elif difficulty == "medium":
            return gph.Image(gph.Point(1060, 583), self.game.assets/"cursor-medium.png")
        elif difficulty == "hard":
            return gph.Image(gph.Point(1060, 619), self.game.assets/"cursor-hard.png")
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