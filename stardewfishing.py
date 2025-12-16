import time
from pathlib import Path
from PIL import Image as PILImage, ImageTk
from lib import radio
from lib import graphics as gph
from scenes import TitleScene, IdleScene, FishingScene, CaughtScene

class Game:
    def __init__(self):
        self.win = gph.GraphWin("Stardew Fishing", 1280, 720, autoflush=False)
        self.basedir = Path(__file__).resolve().parent
        self.assets = self.basedir/"assets"

        self.scenes = {
            "title": TitleScene(self),
            "idle": IdleScene(self),
            "fishing": FishingScene(self),
            "caught": CaughtScene(self)
        }

        self.current_scene = self.scenes["title"]

        self.state = {"i": 0}
        self.frames = self._background_frames()
        self.bg = self.win.create_image(0, 0, anchor="nw", image=self.frames[0])

        self.win.master.protocol("WM_DELETE_WINDOW", self.close_game)

    def change_scene(self, scene):
        self.current_scene.exit_scene()
        self.last_scene = self.current_scene
        self.current_scene = self.scenes[scene]
        self.current_scene.enter_scene()

    def _background_frames(self):
        gif = PILImage.open(self.basedir/"assets"/"background.gif")
        frames = []
        for i in range(gif.n_frames):
            gif.seek(i)
            frame = gif.copy().resize((1280, 720), PILImage.NEAREST)
            frames.append(ImageTk.PhotoImage(frame))
        return frames

    def _background_loop(self):        
        self.win.itemconfig(self.bg, image=self.frames[self.state["i"]])
        self.state["i"] = (self.state["i"] + 1) % len(self.frames)
        self.win.master.after(120, self._background_loop)

    def _loop(self):        
        key = self.win.checkKey().upper()
        if key in ("ESCAPE", "Q"):
            radio.play(self.assets/"audios"/"sfx"/"exit.wav")
            time.sleep(0.25)
            if self.current_scene == self.scenes["title"]:
                self.close_game()
            elif self.current_scene == self.scenes["idle"]:
                self.change_scene("title")
            elif self.current_scene == self.scenes["fishing"]:
                radio.play(self.assets/"audios"/"sfx"/"fish-escape.wav")
                self.change_scene("idle")
            elif self.current_scene == self.scenes["caught"]:
                self.change_scene("idle")

        self.current_scene.update(key)
        self.win.master.after(16, self._loop) # 1/60 = 0.016 (60fps)

    def start_game(self):
        self.current_scene.enter_scene()
        self._background_loop()
        self._loop()
        self.win.master.mainloop()

    def close_game(self):
        radio.stop_all()
        self.win.close()
        self.win.master.quit()
        self.win.master.destroy()

game = Game()
game.start_game()