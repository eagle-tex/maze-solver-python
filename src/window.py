from tkinter import Tk, BOTH, Canvas

from line import Line


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
        line.draw(self.__canvas, fill_color)
