from lib import graphics as gph
import random as rd
from lib import radio
from entities import Sprite, Cursor, Fish, ProgressBar

class FishingScene:
    def __init__(self, game):
        self.game = game
        self.gui = Sprite(gph.Image(gph.Point(1050, 360), self.game.assets/"gui.png"), self.game.win)
        self.fishing = Sprite(gph.Image(gph.Point(625, 350), self.game.assets/"fishing.png"), self.game.win) 
        self.bar = gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270))
        self.timecounter = 0
        self.movement = 1
        self.timeLimitToChangeMovement= rd.randint(0,200)
        
    def enter_scene(self, from_title=False):
        self.fish = Fish(gph.Image(gph.Point(1060, 620), self.game.assets/"fish.png"), self.game.win)
        difficulty = self.fish.getDifficulty()
        rarity = self.fish.getRarity(difficulty)

        self.cursor = Cursor(difficulty, self.game.win, self.game)
        self.progress_bar = ProgressBar(self.bar, self.game.win, self.fish, self.cursor)
        print(f"difficulty: {difficulty}\nrarity: {rarity}\n")

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
            radio.play(self.game.assets/"audios"/"sfx"/"fish-caught.wav")
            return self.game.change_scene("idle")
        elif self.progress_bar.isFishEscaped():
            radio.play(self.game.assets/"audios"/"sfx"/"fish-escape.wav")
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