import unittest

from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells2(self):
        num_cols = 22
        num_rows = 60
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 22
        num_rows = 60
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(
            m1._Maze__cells[0][0].has_top_wall
        )
        self.assertFalse(
            m1._Maze__cells[num_cols-1][num_rows-1].has_bottom_wall
        )

    def test_rest_cells_visited(self):
        num_cols = 22
        num_rows = 60
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        for row in m1._Maze__cells:
            for cell in row:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
