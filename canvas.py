colors = {
    "P": (0, 0, 255),
    "N": (255, 0, 0),
    "NA": (255, 0, 0),
    "SI": (0, 255, 110),
    "SN": (173, 255, 47),
    "SP": (127, 255, 212),
    "M2": (0, 191, 255),
}


def draw_border(border_rect, draw):
    draw.rectangle(
        (border_rect.right, border_rect.top, border_rect.left, border_rect.bottom),
        outline=(0, 0, 0),
        width=15,
    )


def draw_layer(rects, layer, draw):
    for a in rects[layer]:
        draw.rectangle(
            (a.left, a.bottom, a.right, a.top), outline=colors[layer], width=7
        )


def draw_rects(transistors, color, draw):
    for a in transistors:
        draw.rectangle(
            (a.left, a.bottom, a.right, a.top),
            fill=(colors[color] + (128,)),
            outline=(colors[color]),
            width=7,
        )
