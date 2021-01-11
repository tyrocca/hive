from typing import Tuple, Optional
from pydantic import BaseModel

piece_names = ["Q", "B", "A", "G"]


class Point(BaseModel):
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
        return Point(
            int(self.x + x),
            int(self.y + y),
            symbol or self.symbol,
            owner=self.owner,
        )

    def copy(self, symbol, owner=None):
        return Point(self.x, self.y, symbol, owner or self.owner)

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other: "Point") -> bool:
        return self.coordinates == other.coordinates
