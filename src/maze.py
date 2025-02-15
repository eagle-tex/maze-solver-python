import random
from cell import Cell
from window import Window
import time

DEFAULT_SEED = 0
SLEEP_TIME = 0.05  # 0.05

DIRECTIONS_WITH_WALLS = [
    (-1, 0, "UP"),
    (1, 0, "DOWN"),
    (0, -1, "LEFT"),
    (0, 1, "RIGHT"),
]  # Up, Down, Left, Right


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
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self) -> None:
        start_x = self.x1
        start_y = self.y1

        for i in range(self.num_rows):
            current_x: int = start_x
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
        self._animate(0.001)

    def _animate(self, sleep_time=SLEEP_TIME):
        if self.window:
            self.window.redraw()
            time.sleep(sleep_time)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        bottom_right_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        top_left_cell.has_top_wall = False
        self._draw_cell(0, 0)
        bottom_right_cell.has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1)

    def _break_walls_r(self, i: int, j: int) -> None:
        # Mark and draw the current cell right away
        self._cells[i][j].visited = True

        while True:
            possible_directions: list[tuple[int, int]] = []

            # Only add unvisited neighbors
            for di, dj, _ in DIRECTIONS_WITH_WALLS:
                ni, nj = i + di, j + dj  # ni, nj represent the neighbor cell
                # Check if the neighbor is within bounds and unvisited
                if 0 <= ni < self.num_rows and 0 <= nj < self.num_cols:
                    # Check if the neighbor has been visited
                    if not self._cells[ni][nj].visited:
                        possible_directions.append((ni, nj))

            num_possible_dir = len(possible_directions)

            if num_possible_dir == 0:
                self._draw_cell(i, j)
                return

            # Pick a random direction from the remaining ones
            direction_index: int = random.randrange(num_possible_dir)
            next_cell_row, next_cell_col = possible_directions[direction_index]

            # Break walls
            if i + 1 == next_cell_row:  # Moving down
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_cell_row][next_cell_col].has_top_wall = False
            if i - 1 == next_cell_row:  # Moving up
                self._cells[i][j].has_top_wall = False
                self._cells[next_cell_row][next_cell_col].has_bottom_wall = False
            if j + 1 == next_cell_col:  # Moving right
                self._cells[i][j].has_right_wall = False
                self._cells[next_cell_row][next_cell_col].has_left_wall = False
            if j - 1 == next_cell_col:  # Moving left
                self._cells[i][j].has_left_wall = False
                self._cells[next_cell_row][next_cell_col].has_right_wall = False

            self._break_walls_r(next_cell_row, next_cell_col)

    def _reset_cells_visited(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def is_valid_move(
        self, i: int, j: int, ni: int, nj: int, wall_between: str
    ) -> bool:
        if not (0 <= ni < self.num_rows and 0 <= nj < self.num_cols):
            return False  # Destination is out of bounds

        current_cell = self._cells[i][j]
        next_cell = self._cells[ni][nj]

        if next_cell.visited:
            return False  # already visited

        # Check if the wall between the cells permits movement
        if wall_between == "UP" and (
            current_cell.has_top_wall or next_cell.has_bottom_wall
        ):
            return False
        if wall_between == "DOWN" and (
            current_cell.has_bottom_wall or next_cell.has_top_wall
        ):
            return False
        if wall_between == "LEFT" and (
            current_cell.has_left_wall or next_cell.has_right_wall
        ):
            return False
        if wall_between == "RIGHT" and (
            current_cell.has_right_wall or next_cell.has_left_wall
        ):
            return False

        return True

    def undo_move(self, current_cell: Cell, next_cell: Cell):
        current_cell.draw_move(next_cell, True)

    def _solve_r(self, i: int, j: int) -> bool:
        self._animate(0.1)

        # visit the current cell
        self._cells[i][j].visited = True

        # if we are at the end cell, we are done!
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        # for each direction
        for di, dj, wall_between in DIRECTIONS_WITH_WALLS:
            ni, nj = i + di, j + dj

            # if the next cell is valid and is unvisited
            if self.is_valid_move(i, j, ni, nj, wall_between):
                current_cell = self._cells[i][j]
                next_cell = self._cells[ni][nj]

                # Draw the move
                current_cell.draw_move(next_cell)

                # Recurse into the next cell
                if self._solve_r(ni, nj):
                    return True

                # Undo the move if it leads to a dead end
                self.undo_move(current_cell, next_cell)

        # we went the wrong way, let the previous cell know by returning False
        return False

    # create the moves for the solution using a depth-first search
    def solve(self) -> bool:
        return self._solve_r(0, 0)
