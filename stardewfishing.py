import time
import random
import graphics as gph
import os, glob
from PIL import Image as PILImage
from entities import BarEntity, Cursor, Fish

win = gph.GraphWin("Stardew Fishing", 1280, 720)

# arquivos *-resized são temporários
# e servem só pra ir alterando o tamanho sem precisar mexer num editor externo
# assim que definidos, vão substituir tamanhos originais
def resize(path, filename, format, width, height):
    image = PILImage.open(path)
    image = image.resize((width, height))
    image.save(f"assets/{filename}-resized.{format}")
    return image

background = resize("assets/background.png", "background", "png", 1280, 720)
title = resize("assets/title.png", "title", "png", 724, 331)
start = resize("assets/start.png", "start", "png", 523, 57)
gui = resize("assets/gui.png", "gui", "png", 152, 600)
exclamation = resize("assets/exclamation.png", "exclamation", "png", 20, 56)
hit = resize("assets/hit.png", "hit", "png", 185, 75)
cursor_easy = resize("assets/cursor-easy.png", "cursor-easy", "png", 36, 201)
cursor_medium = resize("assets/cursor-medium.png", "cursor-medium", "png", 36, 108)
cursor_hard = resize("assets/cursor-hard.png", "cursor-hard", "png", 36, 36)
fish = resize("assets/fish.png", "fish", "png", 32, 32)

background = gph.Image(gph.Point(640, 360), "assets/background-resized.png")
title = gph.Image(gph.Point(640, 200), "assets/title-resized.png")
start = gph.Image(gph.Point(640, 600), "assets/start-resized.png")
gui = gph.Image(gph.Point(1050, 360), "assets/gui-resized.png")

idle = gph.Image(gph.Point(625, 350), "assets/idle.png")
exclamation = gph.Image(gph.Point(515, 295), "assets/exclamation-resized.png")
hit = gph.Image(gph.Point(645, 265), "assets/hit-resized.png")

fishing = gph.Image(gph.Point(625, 350), "assets/fishing.png")
cursor_easy = gph.Image(gph.Point(1060, 520), "assets/cursor-easy-resized.png")
cursor_medium = gph.Image(gph.Point(1060, 583), "assets/cursor-medium-resized.png")
cursor_hard = gph.Image(gph.Point(1060, 619), "assets/cursor-hard-resized.png")
fishing_progress_bar = gph.Rectangle(gph.Point(1103, 640), gph.Point(1115, 270))
fishing_progress_bar.setFill("green")
fish = gph.Image(gph.Point(1060, 400), "assets/fish-resized.png")
# TODO - select fishes with glob and randomize fish spawn

def is_drawn(obj):
    return obj.canvas is not None

def get_difficulty():
    return random.choice(["easy", "medium", "hard"])

def get_key():
    return win.checkKey().upper()

def get_pos(key_click):
    x = key_click.getX()
    y = key_click.getY()
    return x, y

def is_cursor_climbing(key):
    if key in ("SPACE", "UP"):
        return True
    return False

def cursor_contact_with_fish():
    fish_min_y, fish_max_y = fish.getHitboxMinAndMaxY()
    cursor_min_y, cursor_max_y = cursor.getHitboxMinAndMaxY()
    if cursor_min_y >= fish_min_y and fish_max_y >= cursor_min_y or cursor_max_y >= fish_min_y and cursor_min_y <= fish_min_y:
        return True
    return False
 
def grow_progress_bar():
    global fishing_progress_bar
    start_point = fishing_progress_bar.getP1()
    old_y = fishing_progress_bar.getP2().getY()
    new_y = old_y
    if cursor_contact_with_fish() and old_y >= 75:
        new_y = old_y - 5
    elif old_y <= 640:
        new_y = old_y + 5
    if new_y != old_y:
        fishing_progress_bar.undraw()
        fishing_progress_bar = gph.Rectangle(start_point, gph.Point(1115, new_y))
        fishing_progress_bar.setFill("green")
        fishing_progress_bar.draw(win)
    return fishing_progress_bar

def reset_cursor():
    """
    Atualiza a dificuldade e recria o cursor global.
    """

    global cursor
    difficulty = get_difficulty()
    cursor = Cursor(cursors[difficulty], win)

def title_screen():
    """
    Exibe a tela inicial do jogo.
    Limpa elementos anteriores, mostra o título e aguarda o jogador iniciar
    ou sair do jogo.
    """

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
        fishing_progress_bar.undraw()

    while True:
        click = win.checkMouse()
        key = get_key()

        if click:
            print(get_pos(click))
        elif key in ("ESCAPE", "Q"):
            win.close()
            break

        if not game_started:
            if key in ("RETURN", "KP_ENTER"):
                start_idle()
                game_started = True

def start_idle():
    """
    Controla o estado parado do jogador.
    Aguarda um tempo aleatório até que um peixe seja fisgado
    e verifica se o jogador reage dentro do tempo limite.
    """

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
        fishing_progress_bar.undraw()

    detect_fish = time.time() + random.uniform(2, 5)
    hitted = False

    while True:
        key = get_key()
        if key in ("ESCAPE", "Q"):
            title_screen()
            break

        if time.time() >= detect_fish:
            print("peixe fisgado")

            exclamation.draw(win)
            delay = time.time() + 3

            while time.time() < delay:
                key = get_key()
                if key in ("ESCAPE", "Q"):
                    title_screen()
                    break
                elif key in ("SPACE", "UP"):
                    exclamation.undraw()
                    hitted = True
                    print("foi")
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
    """
    Inicia o modo de pesca após o jogador acertar a fisgada.
    """

    reset_cursor()
    global fishing_progress_bar

    if not is_drawn(gui):
        gui.draw(win)
        fishing.draw(win)
        cursor.draw()
        fish.draw()
        fishing_progress_bar.draw(win)

    if is_drawn(idle):
        idle.undraw()

    speed = 0

    while True:
        key = get_key()
        if key in ("ESCAPE", "Q"):
            title_screen()
            break

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

        fishing_progress_bar = grow_progress_bar()

        cursor.move(speed)
        time.sleep(1/60)

        print(f"y={cursor.getCenterY():.2f},gravity={gravity},speed={speed},key={key}")
        if cursor_contact_with_fish():
            print("FISH CONTACT = True")
        else:
            print("FISH CONTACT = False")

cursors = {
    "easy": cursor_easy,
    "medium": cursor_medium,
    "hard": cursor_hard
}

fish = Fish(fish, win)

background.draw(win)
title_screen()
