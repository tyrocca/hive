import random

from typing import List, Set
from functools import reduce

from .point import Point
from .piece import Piece
from .constants import PLAYER_1, PLAYER_2


class Board:
    padding = 2

    def __init__(self):
        # represents the pieces in pla
        self.pieces = []  # type: List[Piece]

        self.p1_pieces = []  # type: List[Piece]
        self.p2_pieces = []  # type: List[Piece]

        # represents the points that are "in use"
        self.active_points = {}

        # all games start with 2 pieces placed, neither is initialized
        self.first_piece = Piece(Point(0, 0), "0", PLAYER_1)
        self.add_piece(self.first_piece)

        # we choose north but that doesn't actually matter
        self.second_piece = Piece(self.first_piece.north, "1", PLAYER_2)
        self.add_piece(self.second_piece)

    ################################################################################
    ############ Helper properties that should be cached in the future #############
    ################################################################################

    @property
    def min_x(self):
        return min(p.x for p in self.all_available)

    @property
    def max_x(self):
        return max(p.x for p in self.all_available)

    @property
    def min_y(self):
        return min(p.y for p in self.all_available)

    @property
    def max_y(self):
        return max(p.y for p in self.all_available)

    @property
    def all_available(self) -> Set[Point]:
        """ Returns a set of all the possible places that a piece can be placed """
        return (
            reduce(lambda acc, x: acc | x.available_spots, self.pieces, set())
            - self.centers
        )

    def all_player_1(self):
        return (
            reduce(lambda acc, x: acc | x.available_spots, self.pieces, set())
            - self.centers
        )

    @property
    def centers(self) -> Set[Point]:
        return frozenset((p.center for p in self.pieces))

    def add_piece(self, piece: Piece):
        self.pieces.append(piece)
        for point in piece.points:
            self.active_points[point] = point


    def print_board(self):
        grid = []

        # we are going from max y -> min y, then max x to min x
        for y_p in range(self.max_y + self.padding, self.min_y - self.padding, -1):
            row = []
            for x_p in range(self.min_x - self.padding, self.max_x + self.padding):
                point = Point(x_p, y_p)
                if point not in self.active_points:
                    row.append(point)
                else:
                    row.append(self.active_points[point])
            grid.append(row)

        print("-" * (len(grid[0]) + 2))
        for row in grid:
            print("|" + "".join(r.symbol for r in row) + "|")
        print("-" * (len(grid[0]) + 2))
        # return grid

    def test_surround(self):
        l = [
            self.first_piece.north,
            self.first_piece.northeast,
            self.first_piece.southeast,
            self.first_piece.south,
            self.first_piece.southwest,
            self.first_piece.northwest,
        ]
        for idx, p in enumerate(l):
            self.add_piece(Piece(p, str(idx), PLAYER_1))

    def add_random(self):
        random_point = random.choice(list(self.all_available))
        self.add_piece(Piece(random_point, random.choice(piece_names), PLAYER_1))
        self.print_board()

    # def is_complete(self):
    #     p = self.pieces[0]

    #     all_pieces = set(self.pieces)

    #     visited = {}
    #     touched = {p}
    #     while True:
    #         if traversed == all_pieces:
    #             return True
    #         # pieces should hash to the same thing as a point?
    #         for point in p.available_spots:
    #             if point in self.pieces:
    #                 to_visit.add(self.pieces.get(point))

