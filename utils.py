from rect import Rect


def rectsIntersection(rect1, rect2):
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
        if rectsIntersection(element, i):
            key = True
            break
    return key


def getTransistors(rects, p_transistors, n_transistors):
    for i in rects["NA"]:

        # is_contact_window = False

        # for k in rects["CNA"]:
        #     if rectsIntersection(i, k):
        #         if rectsIntersection(i, k).square >= 0.5 * i.square:
        #             is_contact_window = True
        #             break

        # for k in rects["CPA"]:
        #     if rectsIntersection(i, k):
        #         if rectsIntersection(i, k).square >= 0.5 * i.square:
        #             is_contact_window = True
        #             break

        # if intersecton_with_layer(i, rects["CPE"]) or intersecton_with_layer(
        #     i, rects["CNE"]
        # ):
        #     continue

        # for k in rects["CPE"]:
        #     if rectsIntersection(i, k):
        #         is_contact_window = True
        #         break

        # for k in rects["CNE"]:
        #     if rectsIntersection(i, k):
        #         is_contact_window = True
        #         break

        # if is_contact_window:
        #     continue

        # for j in rects["P"]:
        #     # print((i.left, i.bottom), (i.left, i.top), (i.right, i.top), (i.right, i.bottom))
        #     # print((j.left, j.bottom), (j.left, j.top), (j.right, j.top), (j.right, j.bottom))
        #     # print(converter.rectsIntersection(i,j))
        #     # print()
        #     if rectsIntersection(i, j):
        #         is_p_transistor = True

        # if it is a P transistor
        if intersecton_with_layer(i, rects["SP"]):
            p_transistors.append(i)
        elif intersecton_with_layer(i, rects["SN"]):
            n_transistors.append(i)
        else:
            continue
