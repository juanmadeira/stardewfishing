import time
import random

from lib import graphics as gph
from lib import radio

from entities import Sprite

class IdleScene:
    def __init__(self, game):
        self.game = game

        self.idle = Sprite(gph.Image(gph.Point(625, 350), self.game.assets/"idle.png"), self.game.win)
        self.exclamation = Sprite(gph.Image(gph.Point(515, 295), self.game.assets/"exclamation.png"), self.game.win)
        self.hit = Sprite(gph.Image(gph.Point(645, 265), self.game.assets/"hit.png"), self.game.win)

        self.detect_fish = 0
        self.hitted = False

    def enter_scene(self, from_title=False):
        if from_title:
            radio.play(self.game.assets/"audios"/"sfx"/"enter.wav")
            radio.play(self.game.assets/"audios"/"sfx"/"reel.wav")
            radio.play(self.game.assets/"audios"/"sfx"/"pull-water.wav")
            self.play_random_music()

        self.idle.draw()
        self.detect_fish = time.time() + random.uniform(2, 5)

    def play_random_music(self):
        playlist = [
            self.game.assets/"audios"/"playlist"/"in-the-deep-woods.wav",
            self.game.assets/"audios"/"playlist"/"submarine-theme.wav",
            self.game.assets/"audios"/"playlist"/"the-wind-can-be-still.wav"
        ]
        random.shuffle(playlist)
        radio.play(playlist[0])

    def exit_scene(self):
        self.idle.undraw()
        self.exclamation.undraw()
        self.hit.undraw()

    def update(self, key):
        if time.time() >= self.detect_fish:
            radio.play(self.game.assets/"audios"/"sfx"/"fish-bite.wav")
            self.exclamation.draw()

            react_time = time.time() + 3
            while time.time() < react_time and self.game.win.isOpen():
                key = self.game.win.checkKey().upper()
                if key in ("SPACE", "UP"):
                    self.hitted = True
                    break

            self.exclamation.undraw()

            if self.hitted:
                self.hit.draw()
                radio.play(self.game.assets/"audios"/"sfx"/"fish-hit.wav")
                time.sleep(2.5)
                self.hit.undraw()
                return self.game.change_scene("fishing")
            else:
                # TODO: fix music restarting when fish escapes
                return self.game.change_scene("idle")