import reader
from rect import Rect
import converter
import utils
import canvas

# read arrays from file
result = reader.read("data/invertor2.cif")

# print("============== RESULT DICT ==================")
# reader.showResults(result)

# conversion into rectangles
rects = converter.getRectsFromPoints(result)

# print("============== RECTANGLES ==================")
# converter.showRects(rects)

min_left, min_bottom, max_right, max_top, width, height = utils.get_canvas_size(rects)
# print("Canvas size: ", min_left, min_bottom, max_right, max_top, width, height)

adj_rects, width, height = utils.adjust_coordinates(rects, width, height, min_left, min_bottom)

# укропская херня, надо указывать аргументы для создания Rect в неправильном порядке
left_border, bottom_border, right_border, top_border = utils.get_borders(adj_rects)
# print("Borders: ", left_border, bottom_border, right_border, top_border)
# хуета
# border_rect = Rect(right_border, left_border, top_border, bottom_border)
border_rect = Rect(top_border, bottom_border, right_border, left_border)


adj_rects = utils.filter_by_border(adj_rects, border_rect)
# print("============== RECTANGLES AFTER FILTER ==================")
# converter.showRects(adj_rects)

from PIL import Image, ImageDraw

# print("Image size: ", width, height)

layers_keys_dict = {
    "NA": True,
    "P": True,
    "SI": True,
    "SN": True,
    "SP": True,
    "M2": True,
    "M1": True,
    "CM1": False,
    "CNA": False,
    "CPA": False,
    "CPE": False,
    "CNE": False,
    "B1": False,
    "KN": False,
    "CSI": False,
    "CW": False,
}


im = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(im, "RGBA")

# функция рисования контуров слоёв (принимает словарь Bool с названиями слоев)
canvas.draw_frame(layers_keys_dict, adj_rects, draw)


elements_keys_dict = {
    "SI_CONNECTIONS": True,
    "P_TRANSISTORS": True,
    "N_TRANSISTORS": True,
    "P_CHANNELS": True,
    "N_CHANNELS": True,
    "M1_METAL": True,
    "M2_METAL": True,
    "BORDER_RECT": True,
}


elements_dict = utils.get_all_elements(adj_rects, border_rect)

utils.print_all_elements(elements_dict)

squares_dict = utils.get_all_squares(elements_dict, adj_rects, width, height)

utils.print_squares(squares_dict)

#########################################


canvas.draw_chosen_elements(elements_keys_dict, elements_dict, adj_rects, border_rect, draw)


# canvas.draw_si_connections(adj_rects, n_channels, p_channels, draw)

# canvas.draw_rects(p_transistors, "P", 127, draw)
# canvas.draw_rects(p_channels, "SP", 127, draw)

# canvas.draw_rects(n_transistors, "N", 127, draw)
# canvas.draw_rects(n_channels, "SN", 127, draw)

# canvas.draw_rects(m1_metal, "M1", 127, draw)
# canvas.draw_rects(m2_metal, "M2", 127, draw)

# canvas.draw_rects(si_connections, "SI", 127, draw)


im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
