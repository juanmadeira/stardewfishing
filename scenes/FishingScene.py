import random as rd
from lib import gph, radio, ASSETS_DIR, AUDIOS_DIR
from entities import Sprite, Cursor, Fish, ProgressBar

class FishingScene:
    def __init__(self, game):
        self.game = game
        self.gui = Sprite(gph.Image(gph.Point(1050, 360), ASSETS_DIR/"gui.png"), self.game.win)
        self.fishing = Sprite(gph.Image(gph.Point(625, 350), ASSETS_DIR/"fishing.png"), self.game.win)
        self.bar = gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270))
        self.timecounter = 0
        self.movement = 1
        self.timeLimitToChangeMovement= rd.randint(0,200)
        
    def enter_scene(self):
        self.fish = Fish(gph.Image(gph.Point(1060, 400), ASSETS_DIR/"fish.png"), self.game.win)
        self.difficulty = self.fish.getDifficulty()
        self.rarity = self.fish.getRarity(self.difficulty)
        self.cursor = Cursor(self.difficulty, self.game.win)
        self.progress_bar = ProgressBar(self.bar, self.game.win, self.fish, self.cursor)

        self.speed = 0
        self.gui.draw()
        self.fishing.draw()
        self.cursor.draw()
        self.fish.draw()
        self.progress_bar.draw()

    def exit_scene(self):
        self.gui.undraw()
        self.fishing.undraw()
        self.cursor.undraw()
        self.fish.undraw()
        self.progress_bar.undraw()

    def update(self, key):
        self.gravity = 0.3

        if key in ("SPACE", "UP"):
            self.gravity = 0.5
            self.speed += self.gravity
        else:
            self.speed -= 0.23

        if self.cursor.isAtUpperLimit() and self.speed > 0:
            self.speed = 0
        if self.cursor.isAtLowerLimit() and self.speed < 0:
            self.speed = 0

        if self.progress_bar.isFishCaught():
            radio.play(AUDIOS_DIR/"sfx"/"fish-caught.wav")
            return self.game.change_scene("caught")
        elif self.progress_bar.isFishEscaped():
            radio.play(AUDIOS_DIR/"sfx"/"fish-escape.wav")
            return self.game.change_scene("idle")

        self.progress_bar.growProgressBar()
        self.fish.horizontalFlick()
        print(self.timecounter)
        self.timecounter += 1
        self.fish.move(self.movement*6)
        if self.timecounter > self.timeLimitToChangeMovement:
            self.timeLimitToChangeMovement = rd.randint(0,120)
            self.movement = self.fish.randomizeMovement()
            print('mudei a direção em:', self.timecounter,'\nagora estou me movendo em função de',self.movement)
            self.timecounter = 0
        self.cursor.move(self.speed)