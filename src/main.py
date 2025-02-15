from maze import Maze
from window import Window

NUM_ROWS = 24
NUM_COLS = 32
MARGIN = 50
SCREEN_WIDTH = 1600  # 800
SCREEN_HEIGHT = 1200  # 600


def main():
    num_rows = NUM_ROWS
    num_cols = NUM_COLS
    margin = MARGIN
    screen_x = SCREEN_WIDTH
    screen_y = SCREEN_HEIGHT

    cell_size_x = int((screen_x - 2 * margin) / num_cols)
    cell_size_y = int((screen_y - 2 * margin) / num_rows)

    win = Window(screen_x, screen_y)
    # TODO: delete the following line
    print(f"Window size: {win.width} x {win.height}")

    # maze = Maze(200, 100, 8, 8, 50, 50, win)
    # maze = Maze(150, 50, 10, 10, 50, 50, win)
    # maze = Maze(100, 0, 6, 6, 100, 100, win)
    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 1)
    # maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    print(f"num_rows: {maze.num_rows} - num_cols: {maze.num_cols}")

    # Check which cells were visited
    for i in range(maze.num_rows):
        for j in range(maze.num_cols):
            if not maze._cells[i][j].visited:
                print(f"Cell at ({i}, {j}) was not visited!")

            current_cell = maze._cells[i][j]
            print(
                f"Cell {i},{j}: top={current_cell.has_top_wall}, right={current_cell.has_right_wall}, bottom={current_cell.has_bottom_wall}, left={current_cell.has_left_wall}\n"
            )

    # row: int = -1
    # for cell_row in maze._cells:
    #     row += 1
    #     col: int = -1
    #     for cell in cell_row:
    #         col += 1
    #         print(f"Unvisited cell at ({row}, {col})")
    # assert cell.visited, (
    #     "A cell was left unvisited. The maze could have dead ends"
    # )

    win.wait_for_close()


if __name__ == "__main__":
    main()
