from tkinter import Canvas

from point import Point


class Line:
    def __init__(self, start_point: Point, end_point: Point) -> None:
        self.start = start_point
        self.end = end_point

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=fill_color, width=2
        )
