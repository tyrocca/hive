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

    def play(self):
        # you want to ask each player
        self.board.first_move(symbol)

        # get the second move
        self.board.second_move(symbol)

        while True:
            return

""""

How should gameplay work?

- player 1 first_move
- p2 second_move

- offer player options

Turn
- place piece: [player, pieces to place]
- move piece: [player, pieces to move]

what should be returned
what should be stored?

Store:
- game_id
- p1 id
- p2 id
- whose move -> p1 or p2
- turn # ->
- pieces?


/get_turn
- i
- [placeable pieces]: spots to place -- easy
- [movable pieces]:  -> Dict[piece: options: Set[points]]
    - if queen not placed:
        return {}, Queen Not Placed
    - for each piece for a player
        options = {}
        - check if piece is covered -> {}
        if board.breaks_graph(piece):
            return {}
        - if is_beetle
            - add covered by spots -> options |= occupied spots
        - if crawler
            - is stuck -> return -> options
        - if grasshopper
            - options = hoppable_spots(piece)


