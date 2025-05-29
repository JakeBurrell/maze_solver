from tkinter import Tk, BOTH, Canvas
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_a : Point, point_b : Point):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.point_a.x, self.point_a.y, self.point_b.x,
            self.point_b.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, window) -> None:
       self.has_left_wall = True
       self.has_right_wall = True
       self.has_top_wall = True
       self.has_bottom_wall = True
       self.__x1 = -1
       self.__x2 = -1
       self.__y1 = -1
       self.__y2 = -1
       self.__win = window

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        lines = []
        if self.has_left_wall:
            lines.append(Line(Point(x1, y1), Point(x1, y2)))
        if self.has_right_wall:
            lines.append(Line(Point(x2, y1), Point(x2, y2)))
        if self.has_top_wall:
            lines.append(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_bottom_wall:
            lines.append(Line(Point(x1, y2), Point(x2, y2)))
        for line in lines:
            self.__win.draw_line(line, "black")

    def draw_move(self, to_cell, undo=False):
        c_x = self.__x1 + abs((self.__x2 - self.__x1)//2)
        c_y = self.__y1 + abs((self.__y2 - self.__y1)//2)
        to_c_x = to_cell.__x1 + abs((to_cell.__x2 - to_cell.__x1)//2)
        to_c_y = to_cell.__y1 + abs((to_cell.__y2 - to_cell.__y1)//2)
        line = Line(Point(c_x, c_y), Point(to_c_x, to_c_y))
        color = 'red'
        if undo:
            color = 'gray'
        self.__win.draw_line(line, color)

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
        ):
            self.__x1 = x1
            self.__y1 = y1
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.cell_size_x = cell_size_x
            self.cell_size_y = cell_size_y
            self.__win = win
            self.__cells = []

            self.__create_cells()

    def __create_cells(self):

        for row_i in range(self.num_rows):
            col = []
            for row_i in range(self.num_cols):
                col.append(Cell(self.__win))
            self.__cells.append(col)
        for i in range(self.num_rows):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        x_pos = self.__x1 + (i * self.cell_size_x)
        y_pos = self.__y1 + (j * self.cell_size_y)
        self.__cells[i][j].draw(x_pos, y_pos,
        x_pos + self.cell_size_x, y_pos + self.cell_size_y)
        self.__animate()

    def __animate(self):
        if not self.__win:
            return
        self.__win.redraw()
        time.sleep(0.05)


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line: Line, fill_color):
        line.draw(self.__canvas, fill_color)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
