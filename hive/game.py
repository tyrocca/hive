from .board import Board, Piece


class Game:
    def __init__(self):
        self.board = Board()

    def touches_enemy(self, piece):
        pass

    def can_move(self, piece: Piece):
        if piece.covered_by:
            return False
        elif (
            not piece.can_hop
            and not piece.can_climb
            and not board.space_is_crawlable(piece)
        ):
            return False


    """
    where should we put "available spots"
    - on piece
    - on point?
    - on board?

    - given a piece - given an open space check points?
    - we need a point's movement

    """
