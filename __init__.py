import utime
import ujson
import display
import buttons

slFile = open('shoppinglist.json')
data = ujson.load(slFile)
disp = display.open()
offset = 0
highlight = 0

pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)
lastPressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)

items = data['currentState']['items']

def updateDisplay():
    disp.clear()

    for row, item in enumerate(items[offset:4+offset]):
        if row + offset == highlight:
            disp.print(item['name'], posy=20*row, fg=(0,0,0), bg=(255,255,255))
        else:
            disp.print(item['name'], posy=20*row)

    disp.update()

def risingFlank(button):
    global pressed
    global lastPressed
    return pressed & button and not lastPressed & button

def updateButtons():
    global highlight
    global offset
    global pressed
    global lastPressed
    lastPressed = pressed
    pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT)

    if risingFlank(buttons.BOTTOM_LEFT):
        print('left')
        highlight -= 1
        if highlight < 0:
            highlight = 0
        if highlight < offset:
            offset = highlight
    if risingFlank(buttons.BOTTOM_RIGHT):
        print('right')
        highlight += 1
        if highlight >= len(items):
            highlight = len(items) - 1
        if highlight - offset > 3:
            offset = highlight - 3

def mainLoop():
    while(True):
        updateDisplay()
        updateButtons()
        utime.sleep_ms(50)

mainLoop()
