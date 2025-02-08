from tkinter import Tk, BOTH, Canvas

from line import Line
from point import Point


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()  # Create the main window
        self.__root.title("Maze solver")  # Give it a title
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)  # Fill the entire window
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str) -> None:
        line.draw(self.__canvas, fill_color)  # where do I get the canvas from?


def main():
    win = Window(800, 600)
    print(f"Window size: {win.width} x {win.height}")
    pointA = Point(100, 500)
    pointB = Point(500, 500)
    pointC = Point(500, 200)
    pointD = Point(100, 200)
    pointE = Point(300, 50)
    pointJ = Point(275, 500)
    pointK = Point(325, 500)
    pointL = Point(325, 375)
    pointM = Point(275, 375)

    house_color = "blue"
    door_color = "red"
    line1 = Line(pointA, pointB)
    # print(
    #     f"Drawing line from ({line1.start.x}, {line1.start.y}) to ({line1.end.x}, {line1.end.y})"
    # )
    # print("line 1 about to be drawn")
    line2 = Line(pointB, pointC)
    line3 = Line(pointC, pointE)
    line4 = Line(pointE, pointD)
    line5 = Line(pointD, pointA)

    line11 = Line(pointJ, pointM)
    line12 = Line(pointM, pointL)
    line13 = Line(pointL, pointK)

    win.draw_line(line1, house_color)
    win.draw_line(line2, house_color)
    win.draw_line(line3, house_color)
    win.draw_line(line4, house_color)
    win.draw_line(line5, house_color)

    win.draw_line(line11, door_color)
    win.draw_line(line12, door_color)
    win.draw_line(line13, door_color)

    win.wait_for_close()


if __name__ == "__main__":
    main()
