from psychopy import visual

class Shape(visual.Polygon):
    def __init__(self, win, color, position, edges=None):
        if edges is None:
            raise NotImplementedError("This is an abstract class")
        super(Shape, self).__init__(win, edges=edges)
        self.setLineColor(color)
        self.setFillColor(color)
        self.setRadius(0.05)
        self.setPos(position)
        self.setFillColor(color)
        self.setLineColor(color)

class Triangle(Shape):
    name = "Triangle"
    def __init__(self, win, color, position):
        super(Triangle, self).__init__(win, color, position, edges=3)


class Square(Shape):
    name = "Square"
    def __init__(self, win, color, position):
        super(Square, self).__init__(win, color, position, edges=4)
        self.setOri(45)


class Circle(Shape):
    name = "Circle"
    def __init__(self, win, color, position):
        super(Circle, self).__init__(win, color, position, edges=32)
