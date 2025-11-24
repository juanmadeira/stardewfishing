import graphics as gf
from PIL import Image as PILImage

win = gf.GraphWin("Stardew Fishing", 720, 420)

background = gf.Image(gf.Point(360, 210), "assets/background.png")
# arquivos *-resized são temporários
# e servem só pra ir alterando o tamanho sem precisar mexer num editor externo
# assim que definidos, linhas que envolvem PILImage vão ser excluídas
title = PILImage.open("assets/title.png")
title = title.resize((453, 207))
title.save("assets/title-resized.png")
title = gf.Image(gf.Point(360, 110), "assets/title-resized.png")
start = gf.Image(gf.Point(360, 375), "assets/start.png")
gui = PILImage.open("assets/gui.png")
gui = gui.resize((95, 375))
gui.save("assets/gui-resized.png")
gui = gf.Image(gf.Point(600, 210), "assets/gui-resized.png")

background.draw(win)
title.draw(win)
start.draw(win)

def start_game():
    title.undraw()
    start.undraw()
    gui.draw(win)

def get_key(key_click):
    x = key_click.getX()
    y = key_click.getY()

    return x, y

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

