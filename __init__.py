import utime
import ujson
import display
import buttons


class SList:
    def __init__(self, fileName):
        self.fileName = fileName
        slFile = open(fileName)
        self.data = ujson.load(slFile)
        slFile.close()

        self.items = self.data['currentState']['items']

    def removeItem(self, index):
        self.items.pop(index)

class Ui:
    offset = 0
    highlight = 0
    pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT |
      buttons.TOP_RIGHT)
    lastPressed = pressed

    disp = display.open()

def updateDisplay(slist):
    
    # adjust offset
    if Ui.highlight < Ui.offset:
        Ui.offset = Ui.highlight
    if Ui.highlight - Ui.offset > 3:
        Ui.offset = Ui.highlight - 3

    # display list
    Ui.disp.clear()

    for row, item in enumerate(slist.items[Ui.offset:4+Ui.offset]):
        if row + Ui.offset == Ui.highlight:
            Ui.disp.print(item['name'], posy=20*row, fg=(0,0,0), bg=(255,255,255))
        else:
            Ui.disp.print(item['name'], posy=20*row)

    Ui.disp.update()

def risingFlank(button):
    return Ui.pressed & button and not Ui.lastPressed & button

def updateButtons(slist):
    Ui.lastPressed = Ui.pressed
    Ui.pressed = buttons.read(buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT |
      buttons.TOP_RIGHT)

    if risingFlank(buttons.BOTTOM_LEFT):
        Ui.highlight -= 1
        if Ui.highlight < 0:
            Ui.highlight = 0
    if risingFlank(buttons.BOTTOM_RIGHT):
        Ui.highlight += 1
        if Ui.highlight >= len(slist.items):
            Ui.highlight = len(slist.items) - 1
    if risingFlank(buttons.TOP_RIGHT) and len(slist.items):
        slist.removeItem(Ui.highlight)
        if Ui.highlight >= len(slist.items):
            Ui.highlight = len(slist.items) - 1

slist = SList('shoppinglist.json')

def mainLoop():
    while(True):
        updateDisplay(slist)
        updateButtons(slist)
        utime.sleep_ms(50)

mainLoop()
