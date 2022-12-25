from rect import Rect


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
        if rects_intersection(element, i):
            key = True
            break
    return key


def get_transistors(rects):
    n_transistors = []
    p_transistors = []
    for i in rects["NA"]:
        if intersecton_with_layer(i, rects["SP"]):
            p_transistors.append(i)
        elif intersecton_with_layer(i, rects["SN"]):
            n_transistors.append(i)
        else:
            continue
    return p_transistors, n_transistors


def get_channels(rects):
    n_channels = []
    p_channels = []


def rects_union_area(rect1, rect2):
    print()
