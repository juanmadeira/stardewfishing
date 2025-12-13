from lib import graphics as gph
from lib import radio
from entities import Sprite

class TitleScene:
    def __init__(self, game):
        self.game = game

        self.title = Sprite(gph.Image(gph.Point(640, 200), self.game.assets/"title.png"), self.game.win)
        self.start = Sprite(gph.Image(gph.Point(640, 600), self.game.assets/"start.png"), self.game.win)

    def enter_scene(self, from_title=False):
        radio.stop_all()
        radio.play(self.game.assets/"audios"/"title-screen.wav")
        self.title.draw()
        self.start.draw()

    def exit_scene(self):
        radio.stop_all()
        self.title.undraw()
        self.start.undraw()

    def update(self, key):
        if key in ("RETURN", "KP_ENTER"):
            self.game.change_scene("idle", True)