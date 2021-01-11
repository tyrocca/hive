"""
Endpoints

get_board -> returns the board

get_moves[piece] -> returns the moves for a piece

(when a piece is clicked, return possible points)

get_placement[piece_type] -> returns the locations a piece can be placed

place_piece -> piece, (coordinates), force=False (if matching online)

"""

"""
Notes:

How to handle moves that break the board

How to handle placement
- must touch one of the same type
- cannot touch any of opponents (easy)
- can't fit into a space that's bricked (hard)
    - Actually -- look at open spaces
    - for each open space that doesn't touch an opponent
    - check that the open space has at least 2 adjacent open sides


- 2 implementations
  - 1st -- check whether the move is valid (after the move)
  - 2nd -- display possible moves

- create a board 2 -- remove the piece and see if v


if doing the first,
- check for breaks is easy, looks at board 2 and see if

"""


