from typing import Tuple, Optional, NamedTuple
from functools import lru_cache
from .constants import DOUBLE_WIDTH, EDGE_WIDTH


class Point(NamedTuple):
    """
    Class that represents a point on the graph that represents the board.
    We have
    * which represents the corner of a hexagon
    -, / and \\ which represent an edge
    Q, B, A, G which represent a piece
    " " - space which is empty
    """

    x: int
    y: int
    symbol: str = " "
    owner: Optional[str] = None

    @property
    def coordinates(self) -> Tuple[int, int]:
        return (int(self.x), int(self.y))

    def shift(self, x: int = 0, y: int = 0, symbol=None) -> "Point":
        """ Function used to move a single point """
        assert x != 0 or y != 0
        return Point(
            int(self.x + x), int(self.y + y), self.symbol if symbol is None else symbol
        )

    def copy(self, symbol: str, owner=None) -> "Point":
        """ Copies a point """
        return Point(self.x, self.y, symbol)

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other) -> bool:
        return self.coordinates == other.coordinates

    @classmethod
    @lru_cache(64)
    def get_placeable_spots(
        cls, point: "Point"
    ) -> Tuple["Point", "Point", "Point", "Point", "Point", "Point"]:
        """
        This initializes the surround spots that a piece can be placed
        """
        # Then we define the spots around the piece where another piece could
        # be placed. We describe these positions as a compass. These are possible
        # centers of  new points
        north = point.shift(y=DOUBLE_WIDTH, symbol="")
        northeast = point.shift(x=DOUBLE_WIDTH, y=EDGE_WIDTH, symbol="")
        southeast = northeast.shift(y=-DOUBLE_WIDTH, symbol="")
        south = point.shift(y=-DOUBLE_WIDTH, symbol="")
        southwest = point.shift(x=-DOUBLE_WIDTH, y=-EDGE_WIDTH, symbol="")
        northwest = southwest.shift(y=DOUBLE_WIDTH, symbol="")

        return (
            north,
            northeast,
            southeast,
            south,
            southwest,
            northwest,
        )
