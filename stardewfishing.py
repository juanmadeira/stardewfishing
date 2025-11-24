import graphics as gf
from PIL import Image as PILImage

win = gf.GraphWin("Stardew Fishing", 720, 420)

background = gf.Image(gf.Point(360, 210), "assets/background.png")
title = PILImage.open("assets/title.png")
title = title.resize((453, 207))
title.save("assets/title-resized.png")
title = gf.Image(gf.Point(360, 110), "assets/title-resized.png")
start = gf.Image(gf.Point(360, 375), "assets/start.png")

background.draw(win)
title.draw(win)
start.draw(win)

def start_game():
    title.undraw()
    start.undraw()


while True:
    key = win.checkKey()
    key = key.upper()
    if key != "":
        print(key)
    if key == "ESCAPE" or key == "Q":
        break
    if key == "RETURN":
        start_game()
