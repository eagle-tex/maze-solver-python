import random
from maze import Maze
from window import Window

NUM_ROWS = 12
NUM_COLS = 16
MARGIN = 50
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def main():
    num_rows = NUM_ROWS
    num_cols = NUM_COLS
    margin = MARGIN
    screen_x = SCREEN_WIDTH
    screen_y = SCREEN_HEIGHT

    cell_size_x = int((screen_x - 2 * margin) / num_cols)
    cell_size_y = int((screen_y - 2 * margin) / num_rows)

    win = Window(screen_x, screen_y)

    maze = Maze(
        margin,
        margin,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        random.randrange(50),
    )

    # Solve the maze
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
