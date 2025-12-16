from lib import gph

class Sprite:
    def __init__(self, sprite, window: gph.GraphWin):
        self.sprite = sprite
        self.window = window
    
    def draw(self):
        self.sprite.draw(self.window)

    def undraw(self):
        self.sprite.undraw()

    def is_drawn(self):
        return self.sprite.canvas is not None