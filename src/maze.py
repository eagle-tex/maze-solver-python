import random
from cell import Cell
from window import Window
import time

DEFAULT_SEED = 0


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window | None = None,
        seed: int | None = None,
    ) -> None:
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = window
        self._cells: list[list[Cell]] = []
        self.seed = random.seed(seed) if seed else DEFAULT_SEED
        self._create_cells()

    def _create_cells(self) -> None:
        start_x = self.x1
        start_y = self.y1

        for i in range(self.num_rows):
            current_x: int = start_x  # +i*self.cell_size_x
            current_y: int = start_y + i * self.cell_size_y
            cell_row: list[Cell] = []

            for j in range(self.num_cols):
                current_x = start_x + j * self.cell_size_x
                new_cell = Cell(
                    current_x,
                    current_y,
                    current_x + self.cell_size_x,
                    current_y + self.cell_size_y,
                    self.window,
                    True,
                    True,
                    True,
                    True,
                )
                cell_row.append(new_cell)

            self._cells.append(cell_row)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, row: int, col: int) -> None:
        color = "black"
        curr_cell = self._cells[row][col]
        curr_cell.draw(
            self.x1 + col * self.cell_size_x,
            self.y1 + row * self.cell_size_y,
            self.x1 + (col + 1) * self.cell_size_x,
            self.y1 + (row + 1) * self.cell_size_y,
            color,
        )
        self._animate()

    def _animate(self):
        if self.window:
            self.window.redraw()
            time.sleep(0.05)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        top_left_cell.has_top_wall = False
        self._draw_cell(0, 0)
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i, j) -> None:
        current_cell: Cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit: list[tuple[int, int]] = []
            possible_directions: list[tuple[int, int]] = []
            possible_rows = []
            possible_cols = []
            if i == 0:
                possible_rows.append(1)
            elif i == self.num_rows - 1:
                possible_rows.append(i - 1)
            else:
                possible_rows.append(i - 1)
                possible_rows.append(i + 1)

            if j == 0:
                possible_cols.append(1)
            elif j == self.num_cols - 1:
                possible_cols.append(j - 1)
            else:
                possible_cols.append(j - 1)
                possible_cols.append(j + 1)

            for i_val in possible_rows:
                if not self._cells[i_val][j].visited:
                    possible_directions.append((i_val, j))
            for j_val in possible_cols:
                if not self._cells[i][j_val].visited:
                    possible_directions.append((i, j_val))

            num_possible_dir = len(possible_directions)
            if num_possible_dir == 0:
                self._draw_cell(i, j)
                return

            direction = possible_directions[random.randrange(num_possible_dir)]
            next_cell_row: int = direction[0]
            next_cell_col: int = direction[1]
            next_cell = self._cells[next_cell_row][next_cell_col]
            # next_cell_col=direction[1]
            if i == next_cell_row:
                if j < next_cell_col:
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                elif j > next_cell_col:
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
                else:
                    raise Exception("can't have the same column number")
            elif i < next_cell_row:
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            else:
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False

            self._break_walls_r(next_cell_row, next_cell_col)
