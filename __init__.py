import ujson
import display
import buttons

slFile = open('shoppinglist.json')
data = ujson.load(slFile)
disp = display.open()

items = data['currentState']['items']

disp.clear()

for row, item in enumerate(items[:4]):
    disp.print(item['name'], posy=20*row)

disp.update()

