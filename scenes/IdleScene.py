import time
import random as rd
from lib import gph, radio, ASSETS_DIR, AUDIOS_DIR
from entities import Sprite

class IdleScene:
    def __init__(self, game):
        self.game = game
        self.idle = Sprite(gph.Image(gph.Point(625, 350), ASSETS_DIR/"idle.png"), self.game.win)
        self.exclamation = Sprite(gph.Image(gph.Point(515, 295), ASSETS_DIR/"exclamation.png"), self.game.win)
        self.hit = Sprite(gph.Image(gph.Point(645, 265), ASSETS_DIR/"hit.png"), self.game.win)

    def set_fish_wait(self):
        self.hitted = False
        self.fish_detected = False
        self.detect_time = time.time() + rd.uniform(2, 5)

    def play_random_music(self):
        playlist = [
            AUDIOS_DIR/"playlist"/"in-the-deep-woods.wav",
            AUDIOS_DIR/"playlist"/"submarine-theme.wav",
            AUDIOS_DIR/"playlist"/"the-wind-can-be-still.wav"
        ]
        rd.shuffle(playlist)
        radio.play(playlist[0])

    def enter_scene(self):
        self.idle.draw()

        if self.game.last_scene == self.game.scenes["title"]:
            radio.play(AUDIOS_DIR/"sfx"/"enter.wav")
            self.play_random_music()
        if self.game.last_scene == self.game.scenes["title"] or self.game.last_scene == self.game.scenes["caught"]:
            delay = time.time() + 0.5
            while time.time() < delay:
                self.game.win.update()
            self.game.win.master.after(500, radio.play(AUDIOS_DIR/"sfx"/"reel.wav"))
            radio.play(AUDIOS_DIR/"sfx"/"pull-water.wav")

        self.set_fish_wait()

    def exit_scene(self):
        self.idle.undraw()
        self.exclamation.undraw()
        self.hit.undraw()

    def update(self, key):
        if time.time() >= self.detect_time and not getattr(self, "fish_detected"):
            radio.play(AUDIOS_DIR/"sfx"/"fish-bite.wav")
            self.exclamation.draw()
            self.reaction_time = time.time() + 3
            self.punition_time = self.reaction_time + 10
            self.fish_detected = True
            
        if getattr(self, "fish_detected") and not getattr(self, "hitted"):
            if key in ("SPACE", "UP"):
                self.hitted = True
                self.hit_time = time.time()
                self.exclamation.undraw()

            if time.time() >= self.reaction_time:
                self.exclamation.undraw()
                if time.time() >= self.punition_time:
                    return self.game.change_scene("idle")

        if getattr(self, "hitted"):
            if not self.hit.is_drawn():
                radio.play(AUDIOS_DIR/"sfx"/"fish-hit.wav")
                self.hit.draw()

            if time.time() >= self.hit_time + 2:
                self.hit.undraw()
                return self.game.change_scene("fishing")