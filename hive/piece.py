from typing import FrozenSet, Optional, Set, TYPE_CHECKING
from functools import cached_property
from .point import Point
from .constants import PLAYER_1, PLAYER_2, EDGE_WIDTH, HALF_WIDTH

# if TYPE_CHECKING:
#     from .board import Board


class Piece:
    """
    A Piece represents a hive game piece. A Piece is a collection of points.
    A Piece is defined by its center.
    A Piece has available_spots which are the collections of points
        - these are N, NE, SE, S, SW, NE
    A Piece has also has a perimeter which is how it's displayed
    """

    def __init__(
        self, point: Point, symbol: str, owner: str,
    ):
        # core to a piece is its center
        self.owner = owner
        self.symbol = symbol.upper() if self.player_1 else symbol.lower()
        self.center = point.copy(self.symbol, self.owner)

        self.covered_by: Optional[Piece] = None
        self._set_available_spots()

    def __hash__(self):
        return hash(self.center)

    def __eq__(self, other) -> bool:
        return self.center == other

    @property
    def all_covering(self) -> Set["Piece"]:
        covering: Set[Piece] = set()
        ptr = self
        while ptr.covered_by:
            covering.add(ptr.covered_by)
            ptr = ptr.covered_by

        return covering

    @property
    def player_1(self):
        return self.owner == PLAYER_1

    @property
    def player_2(self):
        return self.owner == PLAYER_2

    def can_move(self, board):
        pass

    def move(self, point: Point):
        self.center = point.copy(self.symbol, self.owner)
        self._set_available_spots()
        # clear caches
        del self.points

    def _set_available_spots(self):
        """
        This initializes the surround spots that a piece can be placed
        """
        # Then we define the spots around the piece where another piece could
        # be placed. We describe these positions as a compass. These are possible
        # centers of  new points
        (
            self.north,
            self.northeast,
            self.southeast,
            self.south,
            self.southwest,
            self.northwest,
        ) = Point.get_placeable_spots(self.center)

    @property
    def available_spots(self) -> FrozenSet[Point]:
        return frozenset(Point.get_placeable_spots(self.center))

    def perimeter(self) -> FrozenSet[Point]:
        """
        this initializes the nodes and edges of the piece
        """
        # we then define the points that surround a piece (which would be connected
        # by edges. The points of the hexagon are represented with an '*'
        top_left = self.center.shift(x=-HALF_WIDTH, y=EDGE_WIDTH, symbol="*")
        top_right = top_left.shift(x=EDGE_WIDTH)
        right = top_right.shift(x=EDGE_WIDTH, y=-EDGE_WIDTH)
        bottom_right = right.shift(x=-EDGE_WIDTH, y=-EDGE_WIDTH)
        bottom_left = bottom_right.shift(x=-EDGE_WIDTH)
        left = bottom_left.shift(x=-EDGE_WIDTH, y=EDGE_WIDTH)

        # display the perimeter
        return frozenset((top_left, top_right, left, right, bottom_left, bottom_right))

    def edges(self) -> FrozenSet[Point]:
        # Create the edges
        middle_top = self.center.shift(y=EDGE_WIDTH, symbol="-")
        middle_bottom = self.center.shift(y=-EDGE_WIDTH, symbol="-")
        right_top_side = self.center.shift(x=EDGE_WIDTH, y=HALF_WIDTH, symbol="\\")
        right_bottom_side = self.center.shift(x=EDGE_WIDTH, y=-HALF_WIDTH, symbol="/")
        left_top_side = self.center.shift(x=-EDGE_WIDTH, y=HALF_WIDTH, symbol="/")
        left_bottom_side = self.center.shift(x=-EDGE_WIDTH, y=-HALF_WIDTH, symbol="\\")
        return frozenset(
            (
                middle_top,
                middle_bottom,
                right_top_side,
                right_bottom_side,
                left_top_side,
                left_bottom_side,
            )
        )

    @cached_property
    def points(self) -> FrozenSet[Point]:
        """ returns the points that define a piece """
        return frozenset(self.perimeter() | self.edges())
