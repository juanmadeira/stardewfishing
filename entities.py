import graphics as gph

class BarEntity:
    def __init__(self, sprite, width, height, spawn_x, spawn_y, window):
        self.width = width
        self.height = height
        self.sprite = sprite
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.window = window
        self.element = gph.Image(gph.Point(spawn_x, spawn_y), sprite)
    
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
    