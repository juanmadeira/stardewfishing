import time
import random

from lib import graphics as gph
from entities import Sprite, Cursor, Fish, ProgressBar

class FishingScene:
    def __init__(self, game):
        self.game = game

        self.gui = Sprite(gph.Image(gph.Point(1050, 360), self.game.assets/"gui.png"), self.game.win)
        self.fishing = Sprite(gph.Image(gph.Point(625, 350), self.game.assets/"fishing.png"), self.game.win)

        self.cursor_images = {
            "easy": gph.Image(gph.Point(1060, 520), self.game.assets/"cursor-easy.png"),
            "medium": gph.Image(gph.Point(1060, 583), self.game.assets/"cursor-medium.png"),
            "hard": gph.Image(gph.Point(1060, 619), self.game.assets/"cursor-hard.png"),
        }

        # TODO - select fishes with glob and randomize fish spawn

        fish_sprite = gph.Image(gph.Point(1060, 400), self.game.assets/"fish.png")
        self.fish = Fish(fish_sprite, game.win)

        self.cursor = None
        self.progress_bar = None
        self.speed = 0

    def enter_scene(self):
        difficulty = random.choice(["easy", "medium", "hard"])
        self.cursor = Cursor(self.cursor_images[difficulty], self.game.win)

        bar = gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270))
        self.progress_bar = ProgressBar(bar, self.game.win, self.fish, self.cursor)

        self.gui.draw()
        self.fishing.draw()
        self.cursor.draw()
        self.fish.draw()
        self.progress_bar.draw()
        self.speed = 0

    def exit_scene(self):
        self.gui.undraw()
        self.fishing.undraw()
        self.cursor.undraw()
        self.fish.undraw()
        self.progress_bar.undraw()

    def update(self, key):
        gravity = 0.3
        if key in ("SPACE", "UP"):
            gravity = 0.5
            self.speed += gravity
        else:
            self.speed -= 0.15

        if self.cursor.isAtUpperLimit() and self.speed > 0:
            self.speed = 0
        if self.cursor.isAtLowerLimit() and self.speed < 0:
            self.speed = 0

        self.progress_bar.growProgressBar()
        self.fish.horizontalFlick()
        self.cursor.move(self.speed)
        time.sleep(1/60)