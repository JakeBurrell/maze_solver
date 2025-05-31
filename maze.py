from tkinter import Tk, BOTH, Canvas
import time
import random

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
    def __init__(self, window=None) -> None:
       self.has_left_wall = True
       self.has_right_wall = True
       self.has_top_wall = True
       self.has_bottom_wall = True
       self.visited = False
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
        broken_lines = []
        if self.has_left_wall:
            lines.append(Line(Point(x1, y1), Point(x1, y2)))
        else:
            broken_lines.append(Line(Point(x1, y1), Point(x1, y2)))
        if self.has_right_wall:
            lines.append(Line(Point(x2, y1), Point(x2, y2)))
        else:
            broken_lines.append(Line(Point(x2, y1), Point(x2, y2)))
        if self.has_top_wall:
            lines.append(Line(Point(x1, y1), Point(x2, y1)))
        else:
            broken_lines.append(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_bottom_wall:
            lines.append(Line(Point(x1, y2), Point(x2, y2)))
        else:
            broken_lines.append(Line(Point(x1, y2), Point(x2, y2)))
        if not self.__win:
            return
        for line in lines:
            self.__win.draw_line(line, "black")
        for line in broken_lines:
            self.__win.draw_line(line, "white")


    def draw_move(self, to_cell, undo=False):
        c_x = self.__x1 + abs((self.__x2 - self.__x1)//2)
        c_y = self.__y1 + abs((self.__y2 - self.__y1)//2)
        to_c_x = to_cell.__x1 + abs((to_cell.__x2 - to_cell.__x1)//2)
        to_c_y = to_cell.__y1 + abs((to_cell.__y2 - to_cell.__y1)//2)
        line = Line(Point(c_x, c_y), Point(to_c_x, to_c_y))
        color = 'red'
        if undo:
            color = 'gray'
        if self.__win:
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
            win = None,
            seed = None,
        ):
            self.__x1 = x1
            self.__y1 = y1
            self.num_rows = num_rows
            self.num_cols = num_cols
            self.cell_size_x = cell_size_x
            self.cell_size_y = cell_size_y
            self.__win = win
            self.__cells = []

            if seed:
                random.seed(seed)

            self.__create_cells()
            self.__break_entrance_and_exit()
            self.__break_walls_r(0,0)
            self.__reset_cells_visited()


    def __create_cells(self):
        for col_i in range(self.num_cols):
            row = []
            for row_i in range(self.num_rows):
                row.append(Cell(self.__win))
            self.__cells.append(row)
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.__draw_cell(i, j)


    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0, 0)
        x, y = self.num_cols-1, self.num_rows-1
        self.__cells[x][y].has_bottom_wall = False
        self.__draw_cell(x, y)


    def __draw_cell(self, i, j):
        x_pos = self.__x1 + (i * self.cell_size_x)
        y_pos = self.__y1 + (j * self.cell_size_y)
        self.__cells[i][j].draw(x_pos, y_pos,
        x_pos + self.cell_size_x, y_pos + self.cell_size_y)
        self.__animate()


    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True

        while (True):
            # Cells to visit
            to_visit = []

            # Check Cells to visit next
            # Left
            if i > 0 and not self.__cells[i-1][j].visited:
                to_visit.append((i-1, j))
            # Right
            if i < self.num_cols-1 and not self.__cells[i+1][j].visited:
                to_visit.append((i+1, j))
            # Up
            if j > 0 and not self.__cells[i][j-1].visited:
                to_visit.append((i, j-1))
            # Down
            if j < self.num_rows-1 and not self.__cells[i][j+1].visited:
                to_visit.append((i, j+1))

            if len(to_visit) == 0:
                self.__draw_cell(i,j)
                return

            index_to_visit = random.randrange(len(to_visit))
            next_to_visit = to_visit[index_to_visit]

            # Left
            if next_to_visit[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i-1][j].has_right_wall = False
            # Right
            if next_to_visit[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i+1][j].has_left_wall = False
            # Up
            if next_to_visit[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j-1].has_bottom_wall = False
            # Down
            if next_to_visit[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j+1].has_top_wall = False

            self.__break_walls_r(next_to_visit[0], next_to_visit[1])

    def __reset_cells_visited(self):
        for row in self.__cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        return self.solve_r(0, 0)

    def solve_r(self, i, j):
        self.__animate()
        cell = self.__cells[i][j]
        cell.visited = True

        # Determine end cell
        x_end, y_end = self.num_cols-1, self.num_rows-1
        if x_end == i and y_end == j:
            return True
        directions = {'left': (-1,0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1) }
        for direction, (x,y) in directions.items():
            new_i, new_j = i + x, j + y
            match direction:
                case "left":
                    if i > 0:
                        new_cell = self.__cells[new_i][new_j]
                        if not cell.has_left_wall and not new_cell.visited:
                            cell.draw_move(new_cell)
                            result = self.solve_r(new_i, new_j)
                            if result:
                                return result
                            new_cell.draw_move(cell, True)
                case "right":
                    if i < x_end:
                        new_cell = self.__cells[new_i][new_j]
                        if not cell.has_right_wall and not new_cell.visited:
                            cell.draw_move(new_cell)
                            result = self.solve_r(new_i, new_j)
                            if result:
                                return result
                            new_cell.draw_move(cell, True)
                case "up":
                    if j > 0:
                        new_cell = self.__cells[new_i][new_j]
                        if not cell.has_top_wall and not new_cell.visited:
                            cell.draw_move(new_cell)
                            result = self.solve_r(new_i, new_j)
                            if result:
                                return result
                            new_cell.draw_move(cell, True)
                case "down":
                    if j < y_end:
                        new_cell = self.__cells[new_i][new_j]
                        if not cell.has_bottom_wall and not new_cell.visited:
                            cell.draw_move(new_cell)
                            result = self.solve_r(new_i, new_j)
                            if result:
                                return result
                            new_cell.draw_move(cell, True)
        return False

    def __animate(self):
        if not self.__win:
            return
        self.__win.redraw()
        time.sleep(0.01)


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
