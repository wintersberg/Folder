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


im = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(im, "RGBA")
canvas.draw_layer(adj_rects, "NA", draw)

canvas.draw_layer(adj_rects, "P", draw)

canvas.draw_layer(adj_rects, "SI", draw)

canvas.draw_layer(adj_rects, "SP", draw)

canvas.draw_layer(adj_rects, "SN", draw)

canvas.draw_border(border_rect, draw)

p_transistors, n_transistors = utils.get_transistors(adj_rects)

print("============== P TRANSISTORS ==================")
for i in p_transistors:
    i.printCoords()

print()
print("============== N TRANSISTORS ==================")
for i in n_transistors:
    i.printCoords()

# canvas.draw_n_transistors(n_transistors, draw)

# canvas.draw_p_transistors(p_transistors, draw)

canvas.draw_transistors(p_transistors, "P", draw)

canvas.draw_transistors(n_transistors, "N", draw)


im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
