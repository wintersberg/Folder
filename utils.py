from rect import Rect
import converter
from PIL import Image, ImageDraw
import canvas


def get_canvas_size(rects):

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

    width = max_right - min_left
    height = max_top - min_bottom

    return min_left, min_bottom, max_right, max_top, width, height


def adjust_coordinates(rects, width, height, min_left, min_bottom):

    adj_rects = rects.copy()

    for a in rects:
        adj_rects[a] = []
        for b in rects[a]:
            adj_rects[a].append(
                Rect(
                    (b.right - min_left) // 5,
                    (b.left - min_left) // 5,
                    (b.top - min_bottom) // 5,
                    (b.bottom - min_bottom) // 5,
                )
            )
    width = width // 5
    height = height // 5
    return adj_rects, width, height


def get_borders(rects):
    min_left = 10000000
    min_bottom = 10000000
    max_right = -1000000
    max_top = -1000000
    for b in rects["B1"]:
        if b.left < min_left:
            min_left = b.left
        if b.bottom < min_bottom:
            min_bottom = b.bottom
        if b.right > max_right:
            max_right = b.right
        if b.top > max_top:
            max_top = b.top
    return min_left, min_bottom, max_right, max_top


def rects_intersection(rect1, rect2):
    if rect1.right < rect2.left:
        return False
    if rect1.left > rect2.right:
        return False
    if rect1.top < rect2.bottom:
        return False
    if rect1.bottom > rect2.top:
        return False

    x1 = max(rect1.left, rect2.left)
    x2 = min(rect1.right, rect2.right)
    y1 = max(rect1.bottom, rect2.bottom)
    y2 = min(rect1.top, rect2.top)

    if abs(x1 - x2) * abs(y1 - y2) > 0:
        return Rect(x1, x2, y1, y2)

    return False


def intersecton_with_layer(element, layer_array):
    key = False
    for i in layer_array:
        intersection = rects_intersection(element, i)
        if intersection:
            key = True
            break
    return key, intersection


def get_transistors(rects):
    n_transistors = []
    p_transistors = []
    n_channels = []
    p_channels = []
    for i in rects["NA"]:
        key, intersection = intersecton_with_layer(i, rects["SP"])
        if key:
            p_transistors.append(i)
            p_channels.append(intersection)
            continue
        key, intersection = intersecton_with_layer(i, rects["SN"])
        if key:
            n_transistors.append(i)
            n_channels.append(intersection)
            continue
        else:
            continue
    return p_transistors, n_transistors, p_channels, n_channels


def filter_by_border(rects, border_rect):
    filtered_rects = {}
    for i in rects:
        filtered_rects[i] = []
        for j in rects[i]:
            if (border_rect.is_inside(j)) or (rects_intersection(border_rect, j) == False):
                continue
            else:
                filtered_rects[i].append(Rect(j.right, j.left, j.top, j.bottom))
    return filtered_rects


def arrays_union_square_2(width, height, array1, array2):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(array1, (0, 0, 0), draw)
    canvas.fill_rects(array2, (0, 0, 0), draw)
    # im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
    count = 0
    iter = 1
    for pixel in im.getdata():
        # print(iter, "=", pixel)
        if pixel == (0, 0, 0):
            count += 1
    return count


def arrays_union_square_n(width, height, *arrays):
    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    for i in arrays:
        canvas.fill_rects(i, (0, 0, 0), draw)
    # im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()
    count = 0
    iter = 1
    for pixel in im.getdata():
        # print(iter, "=", pixel)
        if pixel == (0, 0, 0):
            count += 1
    return count


def si_connections_square(width, height, rects, n_channels, p_channels):
    sn_connections = []
    sp_connections = []
    # n_channels = []
    # p_channels = []

    im = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(im, "RGB")
    canvas.fill_rects(rects["SI"], (0, 0, 0), draw)
    canvas.fill_rects(rects["SP"], (0, 0, 0), draw)
    canvas.fill_rects(rects["SN"], (0, 0, 0), draw)
    canvas.fill_rects(n_channels, (255, 255, 255), draw)
    canvas.fill_rects(p_channels, (255, 255, 255), draw)
    # im.rotate(180).transpose(Image.Transpose.FLIP_LEFT_RIGHT).show()

    count = 0
    for pixel in im.getdata():
        if pixel == (0, 0, 0):
            count += 1
    return count


def get_all_elements(adj_rects, border_rect):
    p_transistors, n_transistors, p_channels, n_channels = get_transistors(adj_rects)
    elements_dict = {
        "P_TRANSISTORS": p_transistors,
        "N_TRANSISTORS": n_transistors,
        "P_CHANNELS": p_channels,
        "N_CHANNELS": n_channels,
        "M2_METAL": adj_rects["M2"],
        "M1_METAL": adj_rects["M1"],
        "BORDER_RECT": border_rect,
    }
    return elements_dict


def print_all_elements(elements_dict):
    for a in elements_dict:
        print("=============", a, "=============")
        if type(elements_dict[a]) == list:
            for i in elements_dict[a]:
                i.printCoords()
        else:
            elements_dict[a].printCoords()


def get_all_squares(elements_dict, rects, width, height):

    square_of_n_trans = arrays_union_square_2(width, height, elements_dict["N_TRANSISTORS"], elements_dict["N_TRANSISTORS"])

    square_of_n_channels = arrays_union_square_2(width, height, elements_dict["N_CHANNELS"], elements_dict["N_CHANNELS"])

    square_of_p_trans = arrays_union_square_2(width, height, elements_dict["P_TRANSISTORS"], elements_dict["P_TRANSISTORS"])

    square_of_p_channels = arrays_union_square_2(width, height, elements_dict["P_CHANNELS"], elements_dict["P_CHANNELS"])

    square_of_all_trans = square_of_n_trans + square_of_p_trans

    square_of_all_channels = square_of_n_channels + square_of_p_channels

    square_of_m1_metal = arrays_union_square_2(width, height, elements_dict["M1_METAL"], elements_dict["M1_METAL"])

    square_of_m2_metal = arrays_union_square_2(width, height, elements_dict["M2_METAL"], elements_dict["M2_METAL"])

    square_of_all_metal = arrays_union_square_2(width, height, elements_dict["M1_METAL"], elements_dict["M2_METAL"])

    square_of_si_connections = si_connections_square(
        width, height, rects, elements_dict["N_CHANNELS"], elements_dict["P_CHANNELS"]
    )

    square_of_scheme = arrays_union_square_n(
        width,
        height,
        rects["NA"],
        rects["P"],
        rects["SI"],
        rects["SN"],
        rects["SP"],
        rects["M1"],
        rects["M2"],
    )

    square_of_borders = elements_dict["BORDER_RECT"].square

    squares_dict = {
        "n_trans": square_of_n_trans,
        "p_trans": square_of_p_trans,
        "all_trans": square_of_all_trans,
        "n_channels": square_of_n_channels,
        "p_channels": square_of_p_channels,
        "all_channels": square_of_all_channels,
        "m1_metal": square_of_m1_metal,
        "m2_metal": square_of_m2_metal,
        "all_metal": square_of_all_metal,
        "si": square_of_si_connections,
        "scheme": square_of_scheme,
        "borders": square_of_borders,
    }

    return squares_dict


def print_squares(squares_dict):
    for a in squares_dict:
        print("square of ", a, " = ", squares_dict[a])
