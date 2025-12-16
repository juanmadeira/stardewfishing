from lib import graphics as gph
from lib import radio
from entities import Sprite, Cursor, Fish, ProgressBar

class FishingScene:
    def __init__(self, game):
        self.game = game
        self.gui = Sprite(gph.Image(gph.Point(1050, 360), self.game.assets/"gui.png"), self.game.win)
        self.fishing = Sprite(gph.Image(gph.Point(625, 350), self.game.assets/"fishing.png"), self.game.win)
        self.bar = gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270))
        
    def enter_scene(self):
        self.fish = Fish(gph.Image(gph.Point(1060, 400), self.game.assets/"fish.png"), self.game.win, self.game)
        self.difficulty = self.fish.getDifficulty()
        self.rarity = self.fish.getRarity(self.difficulty)
        self.cursor = Cursor(self.difficulty, self.game.win, self.game)
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
            self.speed -= 0.15

        if self.cursor.isAtUpperLimit() and self.speed > 0:
            self.speed = 0
        if self.cursor.isAtLowerLimit() and self.speed < 0:
            self.speed = 0

        if self.progress_bar.isFishCaught():
            radio.play(self.game.assets/"audios"/"sfx"/"fish-caught.wav")
            return self.game.change_scene("caught")
        elif self.progress_bar.isFishEscaped():
            radio.play(self.game.assets/"audios"/"sfx"/"fish-escape.wav")
            return self.game.change_scene("idle")

        self.progress_bar.growProgressBar()
        self.fish.horizontalFlick()
        self.cursor.move(self.speed)