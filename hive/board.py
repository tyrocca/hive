import random

from typing import Set, Dict, Union, Optional
from functools import reduce

from .point import Point
from .piece import Piece
from .constants import PLAYER_1, PLAYER_2, PIECE_NAMES


class Board:

    padding = 2

    def __init__(self, pieces: Dict[Piece, Piece] = None):
        # represents the pieces in play
        self.pieces: Dict[Piece, Piece] = pieces or {}

        # TODO (tyrocca 2021-01-11): move out of this
        self.first_move()
        self.second_move()

    def first_move(self):
        # all games start with 2 pieces placed, neither is initialized
        self.first_piece = Piece(Point(0, 0), "0", PLAYER_1)
        self.add_piece(self.first_piece)

    def second_move(self):
        # we choose north but that doesn't actually matter
        self.second_piece = Piece(self.first_piece.north, "1", PLAYER_2)
        self.add_piece(self.second_piece)

    def is_complete(self) -> bool:
        """ checks that the board is complete without breaks """
        start = next(iter(self.pieces.values()))
        if start is None:
            return True

        # start at a single piece and ensure found == all pieces
        visited: Set[Union[Piece, Point]] = {start}
        found = {start} | start.all_covering
        points_to_check = set(start.available_spots)

        while points_to_check:
            point = points_to_check.pop()
            visited.add(point)
            # see if a piece exists at that point
            piece: Optional[Piece] = self.pieces.get(point)  # type: ignore
            if piece:
                points_to_check |= piece.available_spots - visited  # type: ignore
                found.add(piece)
                found |= piece.all_covering

        return len(found) == len(self.pieces)

    def get_surrounding(self):
        pass

    @property
    def p1_pieces(self) -> Set[Piece]:
        return filter(lambda p: p.player_1, self.pieces.values())

    @property
    def p2_pieces(self) -> Set[Piece]:
        return filter(lambda p: p.player_2, self.pieces.values())

    @property
    def all_available(self) -> Set[Point]:
        """ Returns a set of all the possible places that a piece can be placed """
        available_spots = reduce(
            lambda acc, x: acc | x.available_spots, self.pieces.values(), set()
        )  # type: Set[Point]
        return available_spots - self.centers

    @property
    def centers(self) -> Set[Piece]:
        return frozenset((p.center for p in self.pieces.values()))  # type: ignore

    def add_piece(self, piece: Piece):
        self.pieces[piece] = piece

    ################################################################################
    #################### Properties that are used for printing #####################
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
    def active_points(self):
        points = dict()  # type: Dict[Union[Piece, Point], Union[Piece, Point]]
        for piece in self.pieces.values():
            points[piece] = piece
            for point in piece.points:
                points[point] = point

        return points

    def print_board(self):
        """ This is what dumps the board """
        grid = []
        active_points = self.active_points

        # we are going from max y -> min y, then max x to min x
        for y_p in range(self.max_y + self.padding, self.min_y - self.padding, -1):
            row = []
            for x_p in range(self.min_x - self.padding, self.max_x + self.padding):
                point = Point(x_p, y_p)
                if point not in active_points:
                    row.append(point)
                else:
                    row.append(active_points[point])
            grid.append(row)

        print("-" * (len(grid[0]) + 2))
        for row in grid:
            print("|" + "".join(r.symbol for r in row) + "|")
        print("-" * (len(grid[0]) + 2))
        # return grid

    def test_surround(self):
        test = [
            self.first_piece.north,
            self.first_piece.northeast,
            self.first_piece.southeast,
            self.first_piece.south,
            self.first_piece.southwest,
            self.first_piece.northwest,
        ]
        for idx, p in enumerate(test):
            self.add_piece(Piece(p, str(idx), PLAYER_1))

    def add_random(self):
        random_point = random.choice(list(self.all_available))
        self.add_piece(Piece(random_point, random.choice(PIECE_NAMES), PLAYER_1))
        self.print_board()
