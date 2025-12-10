from lib import graphics as gph
from lib import radio

class TitleScene:
    def __init__(self, game):
        self.game = game

        self.title = gph.Image(gph.Point(640, 200), self.game.assets/"title.png")
        self.start = gph.Image(gph.Point(640, 600), self.game.assets/"start.png")

    def enter_scene(self):
        radio.stop_all()
        radio.play(self.game.assets/"audios"/"title-screen.wav")
        self.title.draw(self.game.win)
        self.start.draw(self.game.win)

    def exit_scene(self):
        radio.stop_all()
        self.title.undraw()
        self.start.undraw()

    def update(self, key):
        if key in ("RETURN", "KP_ENTER"):
            self.game.change_scene("idle")