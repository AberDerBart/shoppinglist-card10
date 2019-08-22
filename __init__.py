import utime
import ujson
import display
import buttons
import color


class SList:
    def __init__(self, fileName):
        self.fileName = fileName
        slFile = open(fileName)
        self.data = ujson.load(slFile)
        slFile.close()

        self.items = self.data['currentState']['items']
        self.categories = {cat['id']: cat.get('color', '#ffffff')
          for cat in self.data['categories']}

        self.colors = []
        for index, item in enumerate(self.items):
            colorString = self.categories.get(
              item.get('category'), '#ffffff')
            r = int(colorString[1:3], 16)
            g = int(colorString[3:5], 16)
            b = int(colorString[5:7], 16)
            self.colors.append((r, g, b))

    def removeItem(self, index):
        self.items.pop(index)
        self.colors.pop(index)
        self.write()

    def write(self):
        slFile = open(self.fileName, 'w')
        ujson.dump(self.data, slFile)
        slFile.close()

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

    if slist.items:
        for row, item in enumerate(slist.items[Ui.offset:4+Ui.offset]):
            color = slist.colors[row+Ui.offset]
            Ui.disp.rect(0, row * 20, 6, (row + 1) * 20, col=color)
            if row + Ui.offset == Ui.highlight:
                itemString = item['name'] + ' ' * (12 - len(item['name']))
                Ui.disp.print(itemString, posy=20*row, posx=6, fg=(0,0,0),
                  bg=(255,255,255))
            else:
                Ui.disp.print(item['name'], posy=20*row, posx=6)
    else:
        Ui.disp.print('(EMPTY)', posy=30, posx=30)

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


def mainLoop(slist):
    while(True):
        updateDisplay(slist)
        updateButtons(slist)
        utime.sleep_ms(50)

if __name__ == '__main__':
    slist = SList('shoppinglist.json')
    mainLoop(slist)
