from lib import graphics as gph
from entities import Entity

class Fish(Entity):
    def __init__(self, sprite: gph.Image, window: gph.GraphWin):
        super().__init__(sprite, window)
        self.lastHorizontalFlick = 2

    def horizontalFlick(self):
        self.sprite.move(self.lastHorizontalFlick, 0)
        self.lastHorizontalFlick *= -1