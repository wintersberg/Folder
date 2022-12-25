from rect import Rect
import converter


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


def adjust_coordinates(rects, min_left, min_bottom):

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

    return adj_rects


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


def rects_union_square(rect1, rect2):
    square = rect1.square + rect2.square
    intersection = rects_intersection(rect1, rect2)
    if intersection:
        square -= intersection.square
    return square


def arrays_union_square(array1, array2):
    square = 0
    for a in array1:
        square += a.square
        for b in array2:
            square += b.square
            intersection = rects_intersection(a, b)
            if intersection:
                square -= intersection.square
    return square


def array_union_square(array):
    square = 0
    count = 0
    intersections = []
    extrastr = []
    massiv = []
    for a in array:
        for b in array:
            if a != b:
                intersection = rects_intersection(a, b)
                if intersection:
                    count += 1
                    intersections.append(intersection)
    for i in intersections:
        extrastr.append(i.coords_to_string())

    extras = list(dict.fromkeys(extrastr))

    for i in extras:
            left, right, top, bottom = converter.getPointsFromString(i)
            massiv.append(Rect(right, left, top, bottom))

    extraslen = len(massiv)
    for a in array:
        square += a.square
    for b in massiv:
        square -= b.square
    return square, count, extraslen, massiv


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
