import utime
import ujson
import display
import buttons

slFile = open('shoppinglist.json')
data = ujson.load(slFile)
disp = display.open()


items = data['currentState']['items']

class Ui:
    offset = 0
    highlight = 0
    pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
    lastPressed = pressed

def updateDisplay():
    disp.clear()

    for row, item in enumerate(items[Ui.offset:4+Ui.offset]):
        if row + Ui.offset == Ui.highlight:
            disp.print(item['name'], posy=20*row, fg=(0,0,0), bg=(255,255,255))
        else:
            disp.print(item['name'], posy=20*row)

    disp.update()

def risingFlank(button):
    return Ui.pressed & button and not Ui.lastPressed & button

def updateButtons():
    Ui.lastPressed = Ui.pressed
    Ui.pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)

    if risingFlank(buttons.BOTTOM_LEFT):
        Ui.highlight -= 1
        if Ui.highlight < 0:
            Ui.highlight = 0
        if Ui.highlight < Ui.offset:
            Ui.offset = Ui.highlight
    if risingFlank(buttons.BOTTOM_RIGHT):
        Ui.highlight += 1
        if Ui.highlight >= len(items):
            Ui.highlight = len(items) - 1
        if Ui.highlight - Ui.offset > 3:
            Ui.offset = Ui.highlight - 3

def mainLoop():
    while(True):
        updateDisplay()
        updateButtons()
        utime.sleep_ms(50)

mainLoop()
