from line import Line
from point import Point
from window import Window

BACKGROUND_COLOR: str = "#d9d9d9"


class Cell:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        window: Window | None = None,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
    ) -> None:
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._window = window
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited: bool = False

    def get_top_left_corner(self) -> Point:  # Tuple[Point,Point]:
        return Point(self._x1, self._y1)

    def get_top_right_corner(self) -> Point:  # Tuple[Point,Point]:
        return Point(self._x2, self._y1)

    def get_bottom_left_corner(self) -> Point:  # Tuple[Point,Point]:
        return Point(self._x1, self._y2)

    def get_bottom_right_corner(self) -> Point:  # Tuple[Point,Point]:
        return Point(self._x2, self._y2)

    def draw(
        self,
        top_left_x: int,
        top_left_y: int,
        bottom_right_x: int,
        bottom_right_y: int,
        fill_color: str,
    ) -> None:
        top_left_corner: Point = Point(top_left_x, top_left_y)
        bottom_left_corner: Point = Point(top_left_x, bottom_right_y)
        top_right_corner: Point = Point(bottom_right_x, top_left_y)
        bottom_right_corner: Point = Point(bottom_right_x, bottom_right_y)

        if self._window:
            left_wall: Line = Line(top_left_corner, bottom_left_corner)
            if self.has_left_wall:
                self._window.draw_line(left_wall, fill_color)
            else:
                self._window.draw_line(left_wall, BACKGROUND_COLOR)

            top_wall: Line = Line(top_left_corner, top_right_corner)
            if self.has_top_wall:
                self._window.draw_line(top_wall, fill_color)
            else:
                self._window.draw_line(top_wall, BACKGROUND_COLOR)

            right_wall: Line = Line(top_right_corner, bottom_right_corner)
            if self.has_right_wall:
                self._window.draw_line(right_wall, fill_color)
            else:
                self._window.draw_line(right_wall, BACKGROUND_COLOR)

            bottom_wall: Line = Line(bottom_left_corner, bottom_right_corner)
            if self.has_bottom_wall:
                self._window.draw_line(bottom_wall, fill_color)
            else:
                self._window.draw_line(bottom_wall, BACKGROUND_COLOR)

    def draw_move(self, to_cell: "Cell", undo: bool = False):
        if self._window:
            src_cell_center: Point = Point(
                (self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2
            )
            dest_cell_center: Point = Point(
                (to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2
            )
            line_color: str = "red" if not undo else "gray"
            line: Line = Line(src_cell_center, dest_cell_center)
            self._window.draw_line(line, line_color)
