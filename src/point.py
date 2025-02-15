class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # def __eq__(self, other_point: object) -> bool:
    #     if not isinstance(other_point, Point):
    #         return False
    #     if self.x == other_point.x and self.y == other_point.y:
    #         return True
    #     return False
