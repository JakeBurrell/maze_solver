from maze import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    maze = Maze(10, 10, 20, 15, 20, 20, win, 1)
    print("Maze Solved: " + str(maze.solve()))
    win.wait_for_close()


main()
