from lib import graphics as gph
from entities import Sprite

class Entity(Sprite):
    def __init__(self, sprite, window: gph.GraphWin):
        super().__init__(sprite, window)
        
        if hasattr(sprite, "getHeight"):
            self.height = sprite.getHeight()

    def getCenterY(self):
        return self.sprite.getAnchor().getY()
    
    def getHitboxMinAndMaxY(self):
        return (self.getCenterY()-self.height/2, self.getCenterY()+self.height/2)