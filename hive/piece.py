from typing import FrozenSet, Optional, Set, TYPE_CHECKING
from functools import cached_property
from .point import Point
from .constants import PLAYER_1, PLAYER_2

if TYPE_CHECKING:
    from .board import Board

class Piece:
    """
    A Piece represents a hive game piece. A Piece is a collection of points.
    A Piece is defined by its center.
    A Piece has available_spots which are the collections of points
        - these are N, NE, SE, S, SW, NE
    A Piece has also has a perimeter which is how it's displayed
    """

    edge_width = 2
    half_width = int(edge_width / 2)
    double_width = int(edge_width * 2)

    def __init__(
        self,
        point: Point,
        symbol: str,
        owner: str,
    ):
        # core to a piece is its center
        self.owner = owner
        self.symbol = symbol.upper() if self.player_1 else symbol.lower()
        self.center = point.copy(self.symbol, self.owner)

        self.covered_by: Optional[Piece] = None
        self.available_spots: FrozenSet[Point] = frozenset()
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
        self.north = self.center.shift(y=self.double_width, symbol="")
        self.northeast = self.center.shift(
            x=self.double_width, y=self.edge_width, symbol=""
        )
        self.southeast = self.northeast.shift(y=-self.double_width, symbol="")
        self.south = self.center.shift(y=-self.double_width, symbol="")
        self.southwest = self.center.shift(
            x=-self.double_width, y=-self.edge_width, symbol=""
        )
        self.northwest = self.southwest.shift(y=self.double_width, symbol="")

        self.available_spots = frozenset(
            {
                self.north,
                self.northeast,
                self.southeast,
                self.south,
                self.southwest,
                self.northwest,
            }
        )

    def perimeter(self) -> FrozenSet[Point]:
        """
        this initializes the nodes and edges of the piece
        """
        # we then define the points that surround a piece (which would be connected
        # by edges. The points of the hexagon are represented with an '*'
        top_left = self.center.shift(x=-self.half_width, y=self.edge_width, symbol="*")
        top_right = top_left.shift(x=self.edge_width)
        right = top_right.shift(x=self.edge_width, y=-self.edge_width)
        bottom_right = right.shift(x=-self.edge_width, y=-self.edge_width)
        bottom_left = bottom_right.shift(x=-self.edge_width)
        left = bottom_left.shift(x=-self.edge_width, y=self.edge_width)

        # display the perimeter
        return frozenset({top_left, top_right, left, right, bottom_left, bottom_right})

    def edges(self) -> FrozenSet[Point]:
        # Create the edges
        middle_top = self.center.shift(y=self.edge_width, symbol="-")
        middle_bottom = self.center.shift(y=-self.edge_width, symbol="-")
        right_top_side = self.center.shift(
            x=self.edge_width, y=self.half_width, symbol="\\"
        )
        right_bottom_side = self.center.shift(
            x=self.edge_width, y=-self.half_width, symbol="/"
        )
        left_top_side = self.center.shift(
            x=-self.edge_width, y=self.half_width, symbol="/"
        )
        left_bottom_side = self.center.shift(
            x=-self.edge_width, y=-self.half_width, symbol="\\"
        )
        return frozenset(
            {
                middle_top,
                middle_bottom,
                right_top_side,
                right_bottom_side,
                left_top_side,
                left_bottom_side,
            }
        )

    @cached_property
    def points(self) -> FrozenSet[Point]:
        """ returns the points that define a piece """
        return frozenset(self.perimeter() | self.edges())
