from typing import Tuple, Optional, NamedTuple


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

    def shift(self, x: int = 0, y: int = 0, symbol="") -> "Point":
        """ Function used to move a single point """
        assert x != 0 or y != 0
        return Point(int(self.x + x), int(self.y + y), symbol or self.symbol)

    def copy(self, symbol: str, owner=None) -> "Point":
        """ Copies a point """
        return Point(self.x, self.y, symbol)

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other) -> bool:
        return self.coordinates == other.coordinates
