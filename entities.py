import graphics as gph
import random as rd
import time

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
    
    def isDrawn(self):
        return self.sprite.canvas is not None

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
    def __init__(self, sprite: gph.Image, window: gph.GraphWin):
        super().__init__(sprite, window)
        self.lastHorizontalFlick = 2

    def horizontalFlick(self):
        time.sleep(0.2)
        self.sprite.move(self.lastHorizontalFlick, 0)
        self.lastHorizontalFlick *= -1

class ProgressBar():
    def __init__(self, sprite: gph.Rectangle, window: gph.GraphWin, fish: Fish, cursor: Cursor):
        self.sprite = sprite
        self.window = window
        self.fish = fish
        self.cursor = cursor
        self.redValue = 255
        self.greenValue = 172
        self.defaultColor = self.getRgbColor(self.getRedValue(), self.getGreenValue(), 0)
        self.colorStep = 3
        self.placeholder = None

    def growProgressBar(self):
        """
        Atualiza a barra de progresso de pesca.
        """
        if self.getNewY() != self.getOldY():
            self.spawnPlaceholderFishingBar()
            self.updatePosition()
            self.draw()
            self.placeholder.undraw()

    def isGoingUp(self):
        if self.isCursorInContactWithFish():
            return True
        return False

    def isCursorInContactWithFish(self):
        """
        Verifica se o cursor está em contato com o peixe.
        """
        fish_min_y, fish_max_y = self.fish.getHitboxMinAndMaxY()
        cursor_min_y, cursor_max_y = self.cursor.getHitboxMinAndMaxY()
        if cursor_min_y >= fish_min_y and fish_max_y >= cursor_min_y or cursor_max_y >= fish_min_y and cursor_min_y <= fish_min_y:
            return True
        return False

    def updateColor(self):
        red, green = self.getNewRedAndGreenValue()
        self.setRedValue(red)
        self.setGreenValue(green)
        self.sprite.setFill(self.getRgbColor(self.getRedValue(), self.getGreenValue(), 0))

    def spawnPlaceholderFishingBar(self):
        self.placeholder = self.createNewBarOnYPosition(self.getOldY())
        self.placeholder.draw(self.window)

    def updatePosition(self):
        self.undraw()
        self.setSprite(self.createNewBarOnYPosition(self.getNewY()))
        self.updateColor()

    def createNewBarOnYPosition(self, y):
        new_bar = gph.Rectangle(self.getStartPoint(), gph.Point(self.sprite.getP2().getX(), y))
        new_bar.setFill(self.getRgbColor(self.getRedValue(), self.getGreenValue(), 0))

        return new_bar
    
    def draw(self):
        self.sprite.draw(self.window)
    
    def undraw(self):
        self.sprite.undraw()

    def setSprite(self, newSprite):
        self.sprite = newSprite

    def getNewY(self):
        pace = 5
        if self.isGoingUp():
            if self.getOldY() - pace <= 70:
                return 70
            if self.getOldY() > 70:
                return self.getOldY() - pace    
        if self.getOldY() + pace >= 640:
            return 640
        if self.getOldY() < 640:
            return self.getOldY() + pace

    def getOldY(self):
        return self.sprite.getP2().getY()
    
    def getLowerLimit(self):
        return 640
    
    def getUpperLimit(self):
        return 70
    
    def getStartPoint(self):
        return self.sprite.getP1()

    def getNewRedAndGreenValue(self):
        red = self.getRedValue()
        green = self.getGreenValue()
        if self.isGoingUp():
            if green + self.colorStep <= 255:
                green += self.colorStep
            elif red - self.colorStep >= 127:
                red -= self.colorStep
        else:
            if red + self.colorStep <= 255:
                red += self.colorStep
            elif green - self.colorStep >= 50:
                green -= self.colorStep
        
        if green + self.colorStep > 255:
            green = 255
        if green - self.colorStep < 50:
            green = 50
        if red + self.colorStep > 255:
            red = 255
        if red - self.colorStep < 127:
            red = 127
        
        return (red, green)

    # def getNewRedValue(self):
    #     if not self.isGoingUp():
    #         if self.getRedValue() + self.colorStep >= 255:
    #             return 255
    #         return self.getRedValue() + self.colorStep
    #     if self.getRedValue() - self.colorStep <= 127:
    #         return 127
    #     if self.getGreenValue() == 255:
    #         return self.getRedValue() - self.colorStep
            
    # def getNewGreenValue(self):
    #     if self.isGoingUp():
    #         if self.getGreenValue() + self.colorStep >= 255:
    #             return 255
    #         return self.getGreenValue() + self.colorStep
    #     if self.getGreenValue() - self.colorStep <= 50:
    #         return 50
    #     if self.getRedValue() == 255:
    #         return self.getGreenValue() - self.colorStep

    def getGreenValue(self):
        return self.greenValue
    
    def getRedValue(self):
        return self.redValue
    
    def setGreenValue(self, newValue):
        self.greenValue = newValue

    def setRedValue(self, newValue):
        self.redValue = newValue
    
    def getRgbColor(self, r, g, b):
        return gph.color_rgb(r,g,b)