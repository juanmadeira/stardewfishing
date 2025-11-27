import graphics as gph

class BarEntity:
    def __init__(self, sprite: str, spawn_point: gph.Point, window: gph.GraphWin):
        self.sprite = sprite
        self.spawn_point = spawn_point
        self.window = window
        self.element = gph.Image(spawn_point, sprite)
    
    def move(self, amount):
        new_y = self.getY() - amount
        if new_y > 584:
            new_y = 584
        elif new_y < 129:
            new_y = 129
        self.element.move(0, new_y - self.getY())
    
    def draw(self):
        self.element.draw(self.window)

    def undraw(self):
        self.element.undraw()

    def getY(self):
        return self.element.getAnchor().getY()
    
class Cursor(BarEntity):
    def isAtBarLimit(self):
        if self.isAtUpperLimit() or self.isAtLowerLimit():
            return True
        return False
    
    def isAtUpperLimit(self):
        if self.getY() <= 129:
            return True
        return False
    
    def isAtLowerLimit(self):
        if self.getY() >= 584:
            return True
        return False
    