import reader
from rect import Rect
import converter
import utils

# read arrays from file
result = reader.read()

# vivod
print("============== RESULT DICT ==================")
reader.showResults(result)

# conversion into rectangles
rects = converter.getRectsFromPoints(result)

print("============== RECTANGLES ==================")
converter.showRects(rects)

# massiv_n_tran = prosto na
n_transistors = []

# massiv_p_tran = p poverh na
p_transistors = []

utils.getTransistors(rects, p_transistors, n_transistors)

print("============== P TRANSISTORS ==================")
for i in p_transistors:
    i.printCoords()

print()
print("============== N TRANSISTORS ==================")
for i in n_transistors:
    i.printCoords()


from PIL import Image, ImageDraw

# (219, 193, 27))

min_left = 10000000
min_bottom = 10000000
max_right = -1000000
max_top = -1000000

for a in rects:
    for b in rects[a]:
        if b.left < min_left:
            min_left = b.left
        if b.bottom < min_bottom:
            min_bottom = b.bottom
        if b.right > max_right:
            max_right = b.right
        if b.top > max_top:
            max_top = b.top

adj_rects = rects.copy()

for a in rects:
    adj_rects[a] = []
    for b in rects[a]:
        adj_rects[a].append(
            Rect(
                b.right - min_left,
                b.left - min_left,
                b.top - min_bottom,
                b.bottom - min_bottom,
            )
        )


width = max_right - min_left
height = max_top - min_bottom
print("AAAAAAAAAAAAAa ", min_left, min_bottom, width, height)

# Пустой желтый фон.
im = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(im)
for a in adj_rects["NA"]:
    draw.rectangle((a.right, a.top, a.left, a.bottom), outline=(255, 0, 0), width=7)

    # draw.rectangle((a.left, a.top, a.right, a.bottom), outline=(255, 0, 0))
    # draw.rectangle((a.right, a.bottom, a.left, a.top), outline=(255, 0, 0))

    # draw.rectangle((200, 100, 300, 200), outline=(255, 0, 0))
    # draw.ellipse((200, 100, 250, 150), "yellow", "blue")


for a in adj_rects["P"]:
    draw.rectangle((a.left, a.bottom, a.right, a.top), outline=(0, 0, 255), width=7)

im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
