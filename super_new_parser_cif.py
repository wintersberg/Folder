import reader
from rect import Rect
import converter
import utils
import canvas

# read arrays from file
result = reader.read("data/invertor2.cif")

# vivod
print("============== RESULT DICT ==================")
reader.showResults(result)

# conversion into rectangles
rects = converter.getRectsFromPoints(result)

print("============== RECTANGLES ==================")
converter.showRects(rects)


from PIL import Image, ImageDraw

min_left, min_bottom, max_right, max_top, width, height = utils.get_canvas_size(rects)
print("Canvas size: ", min_left, min_bottom, max_right, max_top, width, height)

adj_rects = utils.adjust_coordinates(rects, min_left, min_bottom)

# укропская херня, надо указывать аргументы для создания Rect в неправильном порядке
left_border, bottom_border, right_border, top_border = utils.get_borders(adj_rects)
print("Borders: ", left_border, bottom_border, right_border, top_border)
# border_rect = Rect(right_border, left_border, top_border, bottom_border)
border_rect = Rect(top_border, bottom_border, right_border, left_border)


adj_rects = utils.filter_by_border(adj_rects, border_rect)
print("============== RECTANGLES AFTER FILTER ==================")
converter.showRects(adj_rects)

im = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(im, "RGBA")
canvas.draw_layer(adj_rects, "NA", draw)

canvas.draw_layer(adj_rects, "P", draw)

canvas.draw_layer(adj_rects, "SI", draw)

canvas.draw_layer(adj_rects, "SP", draw)

canvas.draw_layer(adj_rects, "SN", draw)

canvas.draw_layer(adj_rects, "M2", draw)

canvas.draw_border(border_rect, draw)

p_transistors, n_transistors, p_channels, n_channels = utils.get_transistors(adj_rects)

print("============== P TRANSISTORS ==================")
for i in p_transistors:
    i.printCoords()

print()
print("============== P CHANNELS ==================")
for i in p_channels:
    i.printCoords()

print()
print("============== N TRANSISTORS ==================")
for i in n_transistors:
    i.printCoords()

print()
print("============== N CHANNELS ==================")
for i in n_channels:
    i.printCoords()

# square = utils.arrays_union_square(p_transistors, p_channels)
# print()
# print("============== P TRANSISTORS + P CHANNELS ==================")
# print(square / 1000, "k")

print(len(adj_rects["M2"]))
for a in adj_rects["M2"]:
    a.printCoords()

m2_square, inters_count, extraslen, intersections = utils.array_union_square(adj_rects["M2"])
print("m2_square = ", m2_square/1000, "k, inters_count = ", inters_count, "extraslen = ", extraslen,)
for i in intersections:
    i.printCoords()
print()

# temp = [] 
# it = 1
# for x in intersections: 
#     print("current x = ", it)
#     x.printCoords()
#     it += 1
#     if x not in temp: 
#         temp.append(x) 
# intersections2 = temp.copy()

# print()
# # intersections2 = list(set(intersections))
# for i in intersections2:
#     i.printCoords()

canvas.draw_rects(p_transistors, "P", draw)
canvas.draw_rects(p_channels, "SP", draw)

canvas.draw_rects(n_transistors, "N", draw)
canvas.draw_rects(n_channels, "SN", draw)


im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
