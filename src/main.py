from cell import Cell
from window import Window


def main():
    win = Window(800, 600)
    print(f"Window size: {win.width} x {win.height}")

    # Create a few cells and draw them
    cell1 = Cell(50, 50, 100, 100, win, True, False, True, True)
    cell2 = Cell(100, 50, 150, 100, win, False, True, True, False)
    cell3 = Cell(100, 100, 150, 150, win, True, True, False, False)
    cell1.draw(50, 50, 100, 100, "black")
    cell2.draw(100, 50, 150, 100, "blue")
    cell3.draw(100, 100, 150, 150, "red")

    cell1.draw_move(cell2, False)
    cell2.draw_move(cell3, True)

    win.wait_for_close()


if __name__ == "__main__":
    main()
