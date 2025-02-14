from maze import Maze
from window import Window


def main():
    win = Window(800, 600)
    print(f"Window size: {win.width} x {win.height}")

    # maze = Maze(200, 100, 8, 8, 50, 50, win)
    # maze = Maze(150, 50, 10, 10, 50, 50, win)
    # maze = Maze(100, 0, 6, 6, 100, 100, win)
    maze = Maze(200, 100, 4, 4, 100, 100, win, 0)
    maze._break_entrance_and_exit()
    maze._break_walls_r(0, 0)
    print(f"num_rows: {maze.num_rows} - num_cols: {maze.num_cols}")

    # Check which cells were visited
    for i in range(maze.num_rows):
        for j in range(maze.num_cols):
            if not maze._cells[i][j].visited:
                print(f"Cell at ({i}, {j}) was not visited!")

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
