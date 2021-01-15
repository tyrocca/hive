import random

from typing import Set, Dict, Union, Optional, List
from functools import reduce

from .point import Point
from .piece import Piece
from .constants import PLAYER_1, PLAYER_2, PIECE_NAMES


class Board:

    padding = 2
    perimeter = 6

    def __init__(self, pieces: Dict[Piece, Piece] = None):
        # represents the pieces in play
        # only a max of 22 pieces...
        self.pieces: Dict[Piece, Piece] = pieces or {}

        # TODO (tyrocca 2021-01-11): move out of this
        self.first_move()
        self.second_move()

    @property
    def p1_pieces(self) -> Set[Piece]:
        return filter(lambda p: p.player_1, self.pieces.values())

    @property
    def p2_pieces(self) -> Set[Piece]:
        return filter(lambda p: p.player_2, self.pieces.values())

    @property
    def all_open_spots(self) -> Set[Point]:
        """ Returns a set of all the possible places that a piece can be placed """
        surrounding_spots = reduce(
            lambda acc, x: acc | x.available_spots, self.pieces.values(), set()
        )  # type: Set[Point]
        return surrounding_spots - self.centers

    @property
    def all_crawlable_spots(self) -> Set[Point]:
        return {
            spot.copy(symbol="?")
            for spot in self.all_open_spots
            if self.space_is_crawlable(spot)
        }

    @property
    def centers(self) -> Set[Piece]:
        return frozenset((p.center for p in self.pieces.values()))  # type: ignore

    def first_move(self):
        # all games start with 2 pieces placed, neither is initialized
        self.first_piece = Piece(Point(0, 0), "0", PLAYER_1)
        self.add_piece(self.first_piece)

    def second_move(self):
        # we choose north but that doesn't actually matter
        self.second_piece = Piece(self.first_piece.north, "1", PLAYER_2)
        self.add_piece(self.second_piece)

    def is_complete(self, remove_piece) -> bool:
        """ checks that the board is complete without breaks """
        self.pieces.pop(remove_piece)

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

    def space_is_crawlable(self, location: Union[Piece, Point]) -> bool:
        """
        Given a Point
        - see if there are 2 adjacent borders that are free
        """
        points = Point.get_placeable_spots(location)
        for idx, point in enumerate(points):
            if point not in self.pieces:
                adj_point = points[(idx + 1) % self.perimeter]
                assert point != adj_point
                if adj_point not in self.pieces:
                    return True
        return False

    def hoppable_spots(self, origin_piece: Piece):
        """
        Given a starting spot go in a single direction until there
        is a free spot. You must hop at least 1
        """
        options: List[Point] = []
        for direction in Piece.DIRECTIONS:
            # check that at least 1 can be hopped over
            next_point: Point = getattr(origin_piece, direction)
            piece: Optional[Piece] = self.pieces.get(next_point)
            if not piece:
                continue
            while piece:
                next_spot = getattr(piece, direction)
                piece = self.pieces.get(next_spot)
            options.append(next_spot)

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
        open_points = {p: p for p in self.all_open_spots}

        # we are going from max y -> min y, then max x to min x
        for y_p in range(self.max_y + self.padding, self.min_y - self.padding, -1):
            row = []
            for x_p in range(self.min_x - self.padding, self.max_x + self.padding):
                point = Point(x_p, y_p)
                row.append(active_points.get(point) or open_points.get(point) or point)
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
