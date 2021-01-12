from .board import Board, Piece

class Game:

    def __init__(self):
        self.board = Board()

    def touches_enemy(self, piece):
        pass


    def can_move(self, piece: Piece):
        if piece.covered_by:
            return False
        elif not piece.can_hop and not piece.can_climb:
            return
            piece.is_stuck(board)





        board.is_complete()



