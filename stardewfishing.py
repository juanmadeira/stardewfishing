import time
import graphics as gf
from PIL import Image as PILImage

win = gf.GraphWin("Stardew Fishing", 1280, 720)

# arquivos *-resized são temporários
# e servem só pra ir alterando o tamanho sem precisar mexer num editor externo
# assim que definidos, vão substituir tamanhos originais
def resize(path, filename, format, width, height):
    image = PILImage.open(path)
    image = image.resize((width, height))
    image.save(f"assets/{filename}-resized.{format}")
    return image

background = resize("assets/background.png", "background", "png", 1280, 720)
background = gf.Image(gf.Point(640, 360), "assets/background-resized.png")
title = resize("assets/title.png", "title", "png", 724, 331)
title = gf.Image(gf.Point(640, 200), "assets/title-resized.png")
start = resize("assets/start.png", "start", "png", 523, 57)
start = gf.Image(gf.Point(640, 600), "assets/start-resized.png")
gui = resize("assets/gui.png", "gui", "png", 152, 600)
gui = gf.Image(gf.Point(1050, 360), "assets/gui-resized.png")
cursor = resize("assets/cursor-easy.png", "cursor-easy", "png", 36, 108)
cursor = gf.Image(gf.Point(1060, 583), "assets/cursor-easy-resized.png")

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
    if new_y > 584:
        new_y = 584
    elif new_y < 129:
        new_y = 129
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
            if cursor.getAnchor().getY() <= 129:
                gravity = 0
            if gravity >= 0:
                gravity += 0.5
            # for _ in range(60):
            move_cursor(gravity)

    if cursor.getAnchor().getY() >= 584:
        gravity = 0
    elif cursor.getAnchor().getY() <= 129:
        gravity = 0

    if key == "":
        # if time.time() - last_move >= 1/60:
        gravity -= 0.15
        move_cursor(gravity)
        last_move = time.time()

    time.sleep(1/60)
    
    print(f"{key}, y={cursor.getAnchor().getY():.2f},gravity={gravity}")