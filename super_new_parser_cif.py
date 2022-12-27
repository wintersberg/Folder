import reader
from rect import Rect
import converter
import utils
import canvas
from PIL import Image, ImageDraw

# ======================= ПО НАЖАТИЮ КНОПКИ "РАССЧИТАТЬ СХЕМУ" ======================

# read arrays from file
result = reader.read("data/invertor2.cif")

# conversion into rectangles
rects = converter.getRectsFromPoints(result)

min_left, min_bottom, max_right, max_top, width, height = utils.get_canvas_size(rects)

adj_rects, width, height = utils.adjust_coordinates(rects, width, height, min_left, min_bottom, 5)

left_border, bottom_border, right_border, top_border = utils.get_borders(adj_rects)
border_rect = Rect(top_border, bottom_border, right_border, left_border)

adj_rects = utils.filter_by_border(adj_rects, border_rect)

# расчет всех нужных элементов схемы
elements_dict = utils.get_all_elements(adj_rects, border_rect)

utils.print_all_elements(elements_dict)

# расчет площадей (здесь параллельно создаются промежуточные картинки, которые сохраняются в папку images)
squares_dict, report_dict = utils.get_all_squares(elements_dict, adj_rects, width, height)

utils.print_squares(squares_dict)

utils.print_report(report_dict)

# пока всё это считается, в центральной части окна крутится гифка
# когда все рассчиталось, в центральной части окна появляется инфа о схеме, где можно нажать кнопку "Показать на картинке",
# при нажатии на которую будет вызываться функция, соответствующая выбранному элементу из выпадающего списка, например:
utils.show_solution("all_metal")

# это круговые диаграммы, их надо впихнуть на их место в интерфейсе
# но пока что они просто показываются так же, как картинки
utils.show_chart("all_metal")
utils.show_report_chart()

# ======================= ПО НАЖАТИЮ КНОПКИ "НАРИСОВАТЬ КАРТИНКУ" ======================

im = Image.new("RGB", (width, height), (255, 255, 255))
draw = ImageDraw.Draw(im, "RGBA")

# собираем левые чекбоксы
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

# функция рисования контуров слоёв
canvas.draw_frame(layers_keys_dict, adj_rects, draw)

# собираем правые чекбоксы
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

# формирование итоговой цветной картинки
canvas.draw_chosen_elements(elements_keys_dict, elements_dict, adj_rects, border_rect, draw)

im = im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT)

im.save("images/final.jpg", quality=95)

# вывод финальной картиночки
utils.show_final_picture()
