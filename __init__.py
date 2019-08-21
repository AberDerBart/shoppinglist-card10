import utime
import ujson
import display
import buttons

slFile = open('shoppinglist.json')
data = ujson.load(slFile)
disp = display.open()
offset = 0
highlight = 0

items = data['currentState']['items']

def updateDisplay():
    disp.clear()

    for row, item in enumerate(items[offset:4+offset]):
        if row == highlight:
            disp.print(item['name'], posy=20*row, fg=(0,0,0), bg=(255,255,255))
        else:
            disp.print(item['name'], posy=20*row)

    disp.update()

def updateButtons():
    pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
    global highlight

    if pressed & buttons.BOTTOM_LEFT:
        highlight -= 1
        if highlight < 0:
            highlight = 0
    if pressed & buttons.BOTTOM_RIGHT:
        highlight += 1
        if highlight >= len(items):
            highlight = len(items) - 1

def mainLoop():
    while(True):
        updateDisplay()
        updateButtons()
        utime.sleep_ms(50)

mainLoop()
