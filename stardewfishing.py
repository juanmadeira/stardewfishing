import time
import random
import radio
import graphics as gph
import os, glob
from pathlib import Path
from PIL import Image as PILImage, ImageTk
from entities import Cursor, Fish, ProgressBar

basedir = Path(__file__).resolve().parent
win = gph.GraphWin("Stardew Fishing", 1280, 720, autoflush=False)

def resize(path, filename, format, width, height):
    image = PILImage.open(path)
    image = image.resize((width, height))
    image.save(f'{basedir}/"assets"/"{filename}-resized.{format}"')
    return image

title = gph.Image(gph.Point(640, 200), basedir/"assets"/"title.png")
start = gph.Image(gph.Point(640, 600), basedir/"assets"/"start.png")
gui = gph.Image(gph.Point(1050, 360), basedir/"assets"/"gui.png")

idle = gph.Image(gph.Point(625, 350), basedir/"assets/idle.png")
exclamation = gph.Image(gph.Point(515, 295), basedir/"assets"/"exclamation.png")
hit = gph.Image(gph.Point(645, 265), basedir/"assets"/"hit.png")

fishing = gph.Image(gph.Point(625, 350), basedir/"assets"/"fishing.png")
cursor_easy = gph.Image(gph.Point(1060, 520), basedir/"assets"/"cursor-easy.png")
cursor_medium = gph.Image(gph.Point(1060, 583), basedir/"assets"/"cursor-medium.png")
cursor_hard = gph.Image(gph.Point(1060, 619), basedir/"assets"/"cursor-hard.png")
fish = gph.Image(gph.Point(1060, 400), basedir/"assets"/"fish.png")
fish = Fish(fish, win)

#
# TODO - select fishes with glob and randomize fish spawn
#

cursors = {
    "easy": cursor_easy,
    "medium": cursor_medium,
    "hard": cursor_hard
}

gif = PILImage.open(basedir/"assets"/"background.gif")
gif.seek(0)
frames = []
for i in range(gif.n_frames):
    gif.seek(i)
    frame = gif.copy().resize((1280, 720), PILImage.NEAREST)
    frames.append(ImageTk.PhotoImage(frame))
bg = win.create_image(0, 0, anchor="nw", image=frames[0])

state = {"i": 0}
def background():
    win.itemconfig(bg, image=frames[state["i"]])
    state["i"] = (state["i"] + 1) % len(frames)
    win.master.after(120, background)

def is_drawn(obj):
    return obj.canvas is not None

def get_difficulty():
    return random.choice(["easy", "medium", "hard"])

def get_key():
    if win.isOpen():
        return win.checkKey().upper()

def play_random_music():
    playlist = [basedir/"assets"/"audios"/"playlist"/"in-the-deep-woods.wav",
                basedir/"assets"/"audios"/"playlist"/"submarine-theme.wav",
                basedir/"assets"/"audios"/"playlist"/"the-wind-can-be-still.wav"]

    random.shuffle(playlist)
    radio.play(playlist[0])

def exit(option):
    radio.stop_all()
    radio.play(basedir/"assets"/"audios"/"sfx"/"exit.wav")
    if option == "title":
        title_screen()
        return
    if option == "close":
        time.sleep(0.25)
        win.close()
        return

def is_cursor_climbing(key):
    if key in ("SPACE", "UP"):
        return True
    return False

def reset_cursor():
    global cursor
    difficulty = get_difficulty()
    cursor = Cursor(cursors[difficulty], win)

def title_screen():
    if win.isClosed():
        radio.stop_all()
        return

    radio.play(basedir/"assets"/"audios"/"title-screen.wav")

    game_started = False

    if not is_drawn(title):
        title.draw(win)
        start.draw(win)

    if is_drawn(idle):
        idle.undraw()
        exclamation.undraw()
        hit.undraw()

    if is_drawn(gui):
        gui.undraw()
        fishing.undraw()
        cursor.undraw()
        fish.undraw()
        progress_bar.undraw()

    while win.isOpen():
        key = get_key()
        if key in ("ESCAPE", "Q"):
            exit("close")

        if not game_started:
            if key in ("RETURN", "KP_ENTER"):
                game_started = True
                start_idle()

def start_idle():
    if win.isClosed():
        radio.stop_all()
        return
    
    if radio.is_playing():
        radio.stop_all()
        play_random_music()
        radio.play(basedir/"assets"/"audios"/"sfx"/"enter.wav")
        radio.play(basedir/"assets"/"audios"/"sfx"/"reel.wav")
        time.sleep(2)
        radio.play(basedir/"assets"/"audios"/"sfx"/"drop-water.wav")

    if not is_drawn(idle):
        idle.draw(win)

    if is_drawn(title):
        title.undraw()
        start.undraw()

    if is_drawn(gui):
        gui.undraw()
        fishing.undraw()
        cursor.undraw()
        fish.undraw()
        progress_bar.undraw()

    detect_fish = time.time() + random.uniform(2, 5)
    hitted = False

    while win.isOpen():
        key = get_key()
        if key in ("ESCAPE", "Q"):
            exit("title")

        if time.time() >= detect_fish:
            radio.play(basedir/"assets"/"audios"/"sfx"/"fish-bite.wav")
            exclamation.draw(win)
            delay = time.time() + 3

            while time.time() < delay:
                key = get_key()
                if key in ("ESCAPE", "Q"):
                    exit("title")
                elif key in ("SPACE", "UP"):
                    radio.play(basedir/"assets"/"audios"/"sfx"/"fish-hit.wav")
                    hitted = True
                    break
            break

    exclamation.undraw()

    if hitted:
        hit.draw(win)
        time.sleep(2.5)
        hit.undraw()
        start_fishing()
    else:
        start_idle()

def start_fishing():
    if win.isClosed():
        radio.stop_all()
        return

    reset_cursor()
    global progress_bar
    progress_bar = ProgressBar(gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270)), win, fish, cursor)

    if not is_drawn(gui):
        gui.draw(win)
        fishing.draw(win)
        cursor.draw()
        fish.draw()
        progress_bar.draw()
        
    if is_drawn(idle):
        idle.undraw()

    speed = 0

    while win.isOpen():
        key = get_key()
        if key in ("ESCAPE", "Q"):
            exit("title")

        gravity = 0.3
        if is_cursor_climbing(key):
            gravity = 0.5
            speed += gravity
        
        else:
            speed -= 0.15
            if speed > 0 and cursor.isAtUpperLimit():
                speed = 0
                gravity = 0
            if speed <= 0 and cursor.isAtLowerLimit():
                speed = 0
                gravity = 0

        if win.isOpen():
            progress_bar.growProgressBar()
        
        fish.horizontalFlick()

        cursor.move(speed)
        time.sleep(1/60)

background()
title_screen()

if win.isClosed():
    radio.stop_all()