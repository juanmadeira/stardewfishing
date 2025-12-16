import time
from lib import gph, ASSETS_DIR
from entities import Sprite

class CaughtScene:
    def __init__(self, game):
        self.game = game
        self.caught = Sprite(gph.Image(gph.Point(655, 400), ASSETS_DIR/"caught.png"), self.game.win)
        self.balloon = Sprite(gph.Image(gph.Point(520, 240), ASSETS_DIR/"balloon.png"), self.game.win)

    def enter_scene(self):
        self.caught_time = time.time()
        self.rarity = self.game.scenes["fishing"].rarity
        self.fish_specie = self.game.scenes["fishing"].fish.getFishSpecie(self.rarity)
        self.fish = Sprite(gph.Image(gph.Point(456, 247), ASSETS_DIR/"fishes"/self.rarity/f"{self.fish_specie}.png"), self.game.win)

        self.caught.draw()
        self.balloon.draw()
        self.fish.draw()

    def exit_scene(self):
        self.caught.undraw()
        self.balloon.undraw()
        self.fish.undraw()

    def update(self, key):
        if time.time() > self.caught_time + 2.5:
            if key in ("SPACE", "UP"):
                return self.game.change_scene("idle")