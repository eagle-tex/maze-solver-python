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
        self.unvisited_count = self.num_rows * self.num_cols

    def _create_cells(self) -> None:
        start_x = self.x1
        start_y = self.y1
        print(f"Creating maze with {self.num_rows} rows and {self.num_cols} columns")

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
                # TODO: delete
                # print(f"maze creation: i={i}, j={j}")

            self._cells.append(cell_row)

        # TODO: delete
        # print(f"Final _cells length: {len(self._cells)}")
        # print(f"First row length: {len(self._cells[0])}")

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

    def _break_walls_r(self, i: int, j: int) -> None:
        print(f"\nProcessing cell ({i}, {j})")
        current_cell: Cell = self._cells[i][j]

        if current_cell.visited:
            print(f"Cell ({i}, {j}) already visited, returning")
            return  # Skip if this cell was already visited

        # Mark and draw the current cell right away
        current_cell.visited = True
        self.unvisited_count -= 1  # Track remaining unvisited cells
        self._draw_cell(i, j)  # Draw as soon as we visit the cell
        print(
            f"Marked cell ({i}, {j}) as visited. Unvisited count: {self.unvisited_count}"
        )

        # Get all possible directions
        DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        possible_directions: list[tuple[int, int]] = []

        # Only add unvisited neighbors
        for di, dj in DIRECTIONS:
            ni: int = i + di  # ni, nj represent the neighbor cell
            nj: int = j + dj  # ni, nj represent the neighbor cell
            # Check if the neighbor is within bounds and unvisited
            if (
                0 <= ni < self.num_rows and 0 <= nj < self.num_cols
                # and not self._cells[ni][nj].visited
            ):
                neighbor = self._cells[ni][nj]
                # Check if the neighbor has been visited
                if not neighbor.visited:
                    possible_directions.append((ni, nj))

        print(
            f"Cell ({i}, {j}) has {len(possible_directions)} possible directions: {possible_directions}"
        )

        if not possible_directions:
            return

        # Randomize all directions at once
        # random.shuffle(possible_directions)

        # Try each direction
        while possible_directions:
            # Pick a random direction from the remaining ones
            direction_index = random.randrange(len(possible_directions))
            # direction = possible_directions[direction_index]
            next_cell_row, next_cell_col = possible_directions[direction_index]
            # Remove this specific direction after we've used it
            possible_directions.remove((next_cell_row, next_cell_col))
            next_cell = self._cells[next_cell_row][next_cell_col]

            print(
                f"Breaking wall between ({i}, {j}) and ({next_cell_row}, {next_cell_col})"
            )
            print(
                f"Current walls before: top={current_cell.has_top_wall}, right={current_cell.has_right_wall}, bottom={current_cell.has_bottom_wall}, left={current_cell.has_left_wall}"
            )
            print(
                f"Next cell walls before: top={next_cell.has_top_wall}, right={next_cell.has_right_wall}, bottom={next_cell.has_bottom_wall}, left={next_cell.has_left_wall}\n"
            )

            # Break walls
            if i == next_cell_row:  # Moving horizontally
                if j < next_cell_col:  # Moving right
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                elif j > next_cell_col:  # Moving left
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
            elif i < next_cell_row:  # Moving down
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            else:  # Moving up
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False

            print(
                f"Current walls after: top={current_cell.has_top_wall}, right={current_cell.has_right_wall}, bottom={current_cell.has_bottom_wall}, left={current_cell.has_left_wall}"
            )
            print(
                f"Next cell walls after: top={next_cell.has_top_wall}, right={next_cell.has_right_wall}, bottom={next_cell.has_bottom_wall}, left={next_cell.has_left_wall}"
            )

            if not self._cells[next_cell_row][next_cell_col].visited:
                self._break_walls_r(next_cell_row, next_cell_col)
                print(
                    f"Returned from recursive call to ({next_cell_row}, {next_cell_col})\n"
                )
                break
