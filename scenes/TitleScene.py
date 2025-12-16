from lib import gph, radio, ASSETS_DIR, AUDIOS_DIR
from entities import Sprite

class TitleScene:
    def __init__(self, game):
        self.game = game
        self.title = Sprite(gph.Image(gph.Point(640, 200), ASSETS_DIR/"title.png"), self.game.win)
        self.start = Sprite(gph.Image(gph.Point(640, 600), ASSETS_DIR/"start.png"), self.game.win)

    def enter_scene(self):
        radio.stop_all()
        radio.play(AUDIOS_DIR/"title-screen.wav")
        self.title.draw()
        self.start.draw()

    def exit_scene(self):
        radio.stop_all()
        self.title.undraw()
        self.start.undraw()

    def update(self, key):
        if key in ("RETURN", "KP_ENTER"):
            self.game.change_scene("idle")