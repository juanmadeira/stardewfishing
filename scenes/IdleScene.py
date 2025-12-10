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

    def enter_scene(self, from_title=False):
        if from_title:
            radio.play(self.game.assets/"audios"/"sfx"/"enter.wav")
            radio.play(self.game.assets/"audios"/"sfx"/"reel.wav")
            radio.play(self.game.assets/"audios"/"sfx"/"pull-water.wav")
            self.play_random_music()

        self.idle.draw()
        self.hitted = False
        self.fish_detected = False
        self.detect_time = time.time() + random.uniform(2, 5)

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
        if time.time() >= self.detect_time and not getattr(self, "fish_detected"):
            radio.play(self.game.assets/"audios"/"sfx"/"fish-bite.wav")
            self.exclamation.draw()
            self.fish_detected = True

        if getattr(self, "fish_detected"):
            self.reaction_time = time.time() + 3
            
            if key in ("SPACE", "UP"):
                self.hitted = True
                self.hit_time = time.time()
                self.exclamation.undraw()
            if time.time() >= time.time() + self.reaction_time:
                self.exclamation.undraw()
                return self.game.change_scene("idle")

        if getattr(self, "hitted"):
            if not self.hit.is_drawn():
                radio.play(self.game.assets/"audios"/"sfx"/"fish-hit.wav")
                self.hit.draw()

            if time.time() >= self.hit_time + 2:
                self.hit.undraw()
                return self.game.change_scene("fishing")