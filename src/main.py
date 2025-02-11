from maze import Maze
from window import Window


def main():
    win = Window(800, 600)
    print(f"Window size: {win.width} x {win.height}")

    maze = Maze(200, 100, 8, 8, 50, 50, win)
    # maze = Maze(150, 50, 10, 10, 50, 50, win)
    # maze = Maze(100, 0, 6, 6, 100, 100, win)
    maze._create_cells()

    win.wait_for_close()


if __name__ == "__main__":
    main()
