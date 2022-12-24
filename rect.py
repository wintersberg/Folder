class Rect:
    def __init__(self, right, left, top, bottom):
        self.square = abs((right - left) * (top - bottom))
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom

    def printCoords(self):
        print(
            (self.left, self.bottom),
            (self.left, self.top),
            (self.right, self.top),
            (self.right, self.bottom),
            "square = ",
            self.square / 1000,
            "k",
        )

    def getCenter(self):
        x_center = (self.right - self.left) / 2
        y_center = (self.top - self.bottom) / 2
        return (x_center, y_center)
