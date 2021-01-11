from typing import FrozenSet, List
from .point import Point

piece_names = ["Q", "B", "A", "G"]


class Piece:
    edge_width = 2
    half_width = int(edge_width / 2)
    double_width = int(edge_width * 2)

    def __init__(self, point, symbol, owner):
        # core to a piece is its center
        self.center = point.copy(symbol, owner)
        self.symbol = symbol
        self._init_nodes()
        self._init_surrounding_spots()

    def _init_nodes(self):
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

    @property
    def points(self) -> FrozenSet[Point]:
        """ returns the points that define a piece """
        return frozenset(self.perimiter | {self.center} | self.edges)


    def can_move(self, board: "Board") -> bool:
        """
        whether the piece can move
        """
        # you must have 2 adjacent sides free to slide out
        #

        return bool(self.available_spots - board.active_points.keys())

    def possible_moves(self, board: "Board") -> List[Point]:
        if not self.can_move:
            return []
        raise NotImplementedError("Logic for determining moves")

    def touches(self, board: "Board") -> List[Point]:
        touches = []
        for point in self.available_spots:
            occupied = board.active_points[point]
