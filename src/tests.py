import unittest
import random

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_cells_number(self):
        num_rows = 6
        num_cols = 8
        m1 = Maze(50, 50, num_rows, num_cols, 25, 25)
        self.assertEqual(
            len(m1._cells) * len(m1._cells[num_rows - 1]),
            num_rows * num_cols,
        )

    def test_maze_cell_size(self):
        num_rows = 6
        num_cols = 8
        row = random.randrange(num_rows)
        col = random.randrange(num_cols)
        cell_size_x = 25
        cell_size_y = 30
        m1 = Maze(50, 50, num_rows, num_cols, cell_size_x, cell_size_y)
        random_cell = m1._cells[row][col]
        top_left_corner = random_cell.get_top_left_corner()
        bottom_right_corner = random_cell.get_bottom_right_corner()
        self.assertEqual(
            bottom_right_corner.x - top_left_corner.x,
            cell_size_x,
        )
        self.assertEqual(
            bottom_right_corner.y - top_left_corner.y,
            cell_size_y,
        )

    def test_check_top_left_wall_and_bottom_right_wall(self):
        num_rows = 6
        num_cols = 8
        m1 = Maze(50, 50, num_rows, num_cols, 25, 25)
        top_left_cell = m1._cells[0][0]
        bottom_right_cell = m1._cells[num_rows - 1][num_cols - 1]

        self.assertEqual(top_left_cell.has_top_wall, True)
        self.assertEqual(bottom_right_cell.has_bottom_wall, True)

    def test_break_entrance_and_exit(self):
        num_rows = 6
        num_cols = 8
        m1 = Maze(50, 50, num_rows, num_cols, 25, 25)
        m1._break_entrance_and_exit()
        top_left_cell = m1._cells[0][0]
        bottom_right_cell = m1._cells[num_rows - 1][num_cols - 1]

        self.assertEqual(top_left_cell.has_top_wall, False)
        self.assertEqual(bottom_right_cell.has_bottom_wall, False)


if __name__ == "__main__":
    unittest.main()
