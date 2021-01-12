from typing import NamedTuple

PLAYER_1 = 'p1'
PLAYER_2 = 'p2'


class PieceRole(NamedTuple):
    name: str
    symbol: str
    num_pieces: int


PIECE_NAMES = ["Q", "A", "G", "S", "B"]
