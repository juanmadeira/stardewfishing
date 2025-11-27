import time
import random
import graphics as gph
from PIL import Image as PILImage

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
cursor_easy = resize("assets/cursor-easy.png", "cursor-easy", "png", 36, 201)
cursor_medium = resize("assets/cursor-medium.png", "cursor-medium", "png", 36, 108)
cursor_hard = resize("assets/cursor-hard.png", "cursor-hard", "png", 36, 36)

background = gph.Image(gph.Point(640, 360), "assets/background-resized.png")
title = gph.Image(gph.Point(640, 200), "assets/title-resized.png")
start = gph.Image(gph.Point(640, 600), "assets/start-resized.png")
gui = gph.Image(gph.Point(1050, 360), "assets/gui-resized.png")
cursor_easy = gph.Image(gph.Point(1060, 520), "assets/cursor-easy-resized.png")
cursor_medium = gph.Image(gph.Point(1060, 583), "assets/cursor-medium-resized.png")
cursor_hard = gph.Image(gph.Point(1060, 619), "assets/cursor-hard-resized.png")

def get_difficulty():
    return random.choice(["easy", "medium", "hard"])

difficulty = get_difficulty()

if difficulty == "easy":
    top = 175
    bottom = 537
elif difficulty == "medium":
    top = 129
    bottom = 583
elif difficulty == "hard":
    top = 93
    bottom = 619

cursors = {
    "easy": cursor_easy,
    "medium": cursor_medium,
    "hard": cursor_hard
}

cursor = cursors[difficulty]

def is_drawn(obj):
    return obj.canvas is not None

def start_game():
    if not is_drawn(gui):
        title.undraw()
        start.undraw()
        gui.draw(win)
        cursor.draw(win)
    else:
        return False

def get_pos(key_click):
    x = key_click.getX()
    y = key_click.getY()
    return x, y

def move_cursor(amount):
    y = cursor.getAnchor().getY()
    new_y = y - amount
    if new_y > bottom:
        new_y = bottom
    elif new_y < top:
        new_y = top
    cursor.move(0, new_y - y)

background.draw(win)
title.draw(win)
start.draw(win)
last_move = time.time()
gravity = 0

while True:
    click = win.checkMouse()
    key = win.checkKey()
    key = key.upper()

    if click:
        print(get_pos(click))
    elif key != "":
        if key == "ESCAPE" or key == "Q":
            break
        elif key == "RETURN" or key == "KP_ENTER":
            start_game()
        elif key == "SPACE" or key == "UP":
            if gravity < 0:
                gravity = 0
            if cursor.getAnchor().getY() <= top:
                gravity = 0
            if gravity >= 0:
                gravity += 0.5
            move_cursor(gravity)

    if cursor.getAnchor().getY() >= bottom:
        gravity = 0
    elif cursor.getAnchor().getY() <= top:
        gravity = 0

    if key == "":
        gravity -= 0.15
        move_cursor(gravity)
        last_move = time.time()

    time.sleep(1/60)
    
    print(f"{key}, y={cursor.getAnchor().getY():.2f},gravity={gravity}")
