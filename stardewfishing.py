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

def start_game():
    title.undraw()
    start.undraw()
    gui.draw(win)

def get_key(key_click):
    x = key_click.getX()
    y = key_click.getY()

    return x, y

background.draw(win)
title.draw(win)
start.draw(win)

while True:
    click = win.checkMouse()
    key = win.checkKey()
    key = key.upper()

    if click:
        print(get_key(click))
    if key != "":
        print(key)
    if key == "ESCAPE" or key == "Q":
        break
    if key == "RETURN":
        start_game()

