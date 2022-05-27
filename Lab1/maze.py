from typing import NamedTuple, List, Dict
from math import sqrt


class Sign(object):
    CONST_WALL = "x"


class Point(NamedTuple):
    x: int
    y: int


class Maze:
    def __init__(self, row, col, matrix: List, start: Point, end: Point, bonus_points_dict: Dict[Point,float]=None):
        self.row = row
        self.col = col
        self.matrix = matrix
        self.start = start
        self.end = end
        self.bonus_points_dict = bonus_points_dict

    def valid_position(self, pos_x, pos_y):
        return pos_x >= 0 and pos_x < self.row and pos_y >= 0 and pos_y < self.col and self.matrix[pos_x][pos_y] != Sign.CONST_WALL

    def valid_path(self, p: Point):
        neighbors = [
            (p.x - 1, p.y),
            (p.x, p.y + 1),
            (p.x + 1, p.y),
            (p.x, p.y - 1)
        ]

        path: List[Point] = []
        for pos_x, pos_y in neighbors:
            if self.valid_position(pos_x, pos_y):
                path.append(Point(pos_x, pos_y))
        return path

    def manhattan_distance(self, p: Point):
        return abs(self.end.x-p.x) + abs(self.end.y-p.y)

    def euclidean_distance(self, p: Point):
        return sqrt((self.end.x-p.x)*(self.end.x-p.x)+(self.end.y-p.y)*(self.end.y-p.y))

    def weight(self, p: Point, bonus_points_dict: Dict[Point,float] = None):
        result = 1
        if bonus_points_dict != None and  p in bonus_points_dict.keys():
            result = bonus_points_dict[p]
            del bonus_points_dict[p]
        return result
