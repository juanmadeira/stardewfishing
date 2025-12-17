import time
from lib import gph, ASSETS_DIR
from entities import Sprite

class CaughtScene:
    def __init__(self, game):
        self.game = game
        self.caught = Sprite(gph.Image(gph.Point(655, 400), ASSETS_DIR/"caught.png"), self.game.win)
        self.balloon = Sprite(gph.Image(gph.Point(520, 240), ASSETS_DIR/"balloon.png"), self.game.win)

    def make_text(self, point, text, size, face="courier", style=None, color=None):
        text = gph.Text(point, text)
        text.setSize(size)
        text.setFace(face)
        if style:
            text.setStyle(style)
        if color:
            text.setTextColor(color)
        return text

    def enter_scene(self):
        self.caught_time = time.time()
        self.rarity = self.game.scenes["fishing"].rarity
        self.rarity_color = self.game.scenes["fishing"].fish.getRarityColor(self.rarity)
        self.fish_specie = self.game.scenes["fishing"].fish.getFishSpecie(self.rarity)
        self.fish = Sprite(gph.Image(gph.Point(456, 247), ASSETS_DIR/"fishes"/self.rarity/f"{self.fish_specie}.png"), self.game.win)

        self.fish_name = Sprite(self.make_text(gph.Point(525, 180), self.fish_specie.replace("-", " ").title(), 15, style="bold"), self.game.win)
        self.rarity_title = Sprite(self.make_text(gph.Point(560, 215), "Rarity:", 13), self.game.win)
        self.rarity_text = Sprite(self.make_text(gph.Point(560, 235),f" {self.rarity.title()}", 13, color=self.rarity_color), self.game.win)

        self.caught.draw()
        self.balloon.draw()
        self.fish.draw()
        self.fish_name.draw()
        self.rarity_title.draw()
        self.rarity_text.draw()

    def exit_scene(self):
        self.caught.undraw()
        self.balloon.undraw()
        self.fish.undraw()
        self.fish_name.undraw()
        self.rarity_title.undraw()
        self.rarity_text.undraw()

    def update(self, key):
        if time.time() > self.caught_time + 2.5:
            if key in ("SPACE", "UP"):
                return self.game.change_scene("idle")