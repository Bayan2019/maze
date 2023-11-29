from tkinter import Tk, BOTH, Canvas

class Window():
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("MAZE of Searching")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color='red'):
        line.draw(self.__canvas, fill_color)
    
    def draw_cell(self, cell, fill_color='black'):
        cell.draw(self.__canvas, fill_color)

class Point():
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color='red'):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)
        canvas.pack(fill=BOTH, expand=1)

class Cell:
    def __init__(self, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._p1 = Point()
        self._p2 = Point()
        self._win = win

    def draw(self, p1, p2, fill_color='black'):
        self._p1 = p1
        self._p2 = p2
        if self.has_left_wall:
            line = Line(p1, Point(p1.x, p2.y))
            self._win.draw_line(line, fill_color)
        else:
            line = Line(p1, Point(p1.x, p2.y))
            self._win.draw_line(line, "white")

        if self.has_top_wall:
            line = Line(p1, Point(p2.x, p1.y))
            self._win.draw_line(line, fill_color)
        else:
            line = Line(p1, Point(p2.x, p1.y))
            self._win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(p2.x, p1.y), p2)
            self._win.draw_line(line, fill_color)
        else:
            line = Line(Point(p2.x, p1.y), p2)
            self._win.draw_line(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(p1.x, p2.y), p2)
            self._win.draw_line(line, fill_color)
        else:
            line = Line(Point(p1.x, p2.y), p2)
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if undo:
            fill='gray'
        else:
            fill='red'

        p1 = Point((self._p1.x + self._p2.x)/2, (self._p1.y + self._p2.y)/2)
        p2 = Point((to_cell._p1.x + to_cell._p2.x)/2, (to_cell._p1.y + to_cell._p2.y)/2)

        # line = Line(p1=p1, p2=p2)
        # self._win.draw_line(line, fill)

        # moving left
        if self._p1.x > to_cell._p1.x:
            line = Line(Point(self._p1.x, p1.y), p1)
            self._win.draw_line(line, fill)
            line = Line(p2, Point(to_cell._p2.x, p2.y))
            self._win.draw_line(line, fill)

        # moving right
        elif self._p1.x < to_cell._p1.x:
            line = Line(p1, Point(self._p2.x, p1.y))
            self._win.draw_line(line, fill)
            line = Line(Point(to_cell._p1.x, p2.y), p2)
            self._win.draw_line(line, fill)

        # moving up
        elif self._p1.y > to_cell._p1.y:
            line = Line(p1, Point(p1.x, self._p1.y))
            self._win.draw_line(line, fill)
            line = Line(Point(p2.x, to_cell._p2.y), p2)
            self._win.draw_line(line, fill)

        # moving down
        elif self._p1.y < to_cell._p1.y:
            line = Line(p1, Point(p1.x, self._p2.y))
            self._win.draw_line(line, fill)
            line = Line(p2, Point(p2.x, to_cell._p1.y))
            self._win.draw_line(line, fill)