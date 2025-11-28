import graphics as gph
import random as rd

class BarEntity:
    def __init__(self, sprite: gph.Image, window: gph.GraphWin):
        self.sprite = sprite
        self.window = window
        self.height = self.sprite.getHeight()

    def move(self, amount):
        new_y = self.getCenterY() - amount
        if new_y > self.getLowerLimit():
            new_y = self.getLowerLimit()
        elif new_y < self.getUpperLimit():
            new_y = self.getUpperLimit()
        self.sprite.move(0, new_y - self.getCenterY())
    
    def draw(self):
        self.sprite.draw(self.window)

    def undraw(self):
        self.sprite.undraw()

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
    
    def getCenterY(self):
        return self.sprite.getAnchor().getY()
    
    def getHitboxMinAndMaxY(self):
        return (self.getCenterY()-self.height/2, self.getCenterY()+self.height/2)

    def getLowerLimit(self):
        return 637 - self.height/2
    
    def getUpperLimit(self):
        return 74 + self.height/2

class Cursor(BarEntity):
    pass
class Fish(BarEntity):
    pass


        