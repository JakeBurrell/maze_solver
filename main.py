from maze import Window, Point, Line, Cell

def main():
    win = Window(800, 600)

    cell = Cell(win)
    cell2 = Cell(win)

    cell.draw(10, 10, 50, 50)
    cell2.draw(100, 100, 140, 140)

    cell.draw_move(cell2, undo=True)

    win.wait_for_close()


main()
