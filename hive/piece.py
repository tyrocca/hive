from typing import FrozenSet
from pydantic import BaseModel
from .point import Point

piece_names = ["Q", "B", "A", "G"]


class Piece(BaseModel):

    edge_width = 2
    half_width = int(edge_width / 2)
    double_width = int(edge_width * 2)



    def __init__(self, point: Point, symbol: str, owner: str):
        # core to a piece is its center
        self.center = point.copy(symbol, owner)
        self.symbol = symbol

        self._init_surrounding_spots()

        # these are for display purposes
        self._init_display()

    def _init_surrounding_spots(self):
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

    def _init_display(self):
        """
        this initializes the nodes and edges of the piece
        """
        # we then define the points that surround a piece (which would be connected
        # by edges. The points of the hexagon are represented with an '*'
        self.top_left = self.center.shift(
            x=-self.half_width, y=self.edge_width, symbol="*"
        )
        self.top_right = self.top_left.shift(x=self.edge_width)
        self.right = self.top_right.shift(x=self.edge_width, y=-self.edge_width)
        self.bottom_right = self.right.shift(x=-self.edge_width, y=-self.edge_width)
        self.bottom_left = self.bottom_right.shift(x=-self.edge_width)
        self.left = self.bottom_left.shift(x=-self.edge_width, y=self.edge_width)

        # display the perimeter
        self.perimiter = frozenset(
            {
                self.top_left,
                self.top_right,
                self.left,
                self.right,
                self.bottom_left,
                self.bottom_right,
            }
        )  # type: FrozenSet[Point]

        # Create the edges
        self.middle_top = self.center.shift(y=self.edge_width, symbol="-")
        self.middle_bottom = self.center.shift(y=-self.edge_width, symbol="-")
        self.right_top_side = self.center.shift(
            x=self.edge_width, y=self.half_width, symbol="\\"
        )
        self.right_bottom_side = self.center.shift(
            x=self.edge_width, y=-self.half_width, symbol="/"
        )
        self.left_top_side = self.center.shift(
            x=-self.edge_width, y=self.half_width, symbol="/"
        )
        self.left_bottom_side = self.center.shift(
            x=-self.edge_width, y=-self.half_width, symbol="\\"
        )

        self.edges = frozenset(
            {
                self.middle_top,
                self.middle_bottom,
                self.right_top_side,
                self.right_bottom_side,
                self.left_top_side,
                self.left_bottom_side,
            }
        )

    @property
    def points(self) -> FrozenSet[Point]:
        """ returns the points that define a piece """
        return frozenset(self.perimiter | {self.center} | self.edges)
