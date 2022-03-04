# planning creation of chess game

- creating game straight from pygame, no terminal stuff needed

- using object oriented paradigm
    - one class for a general piece, and inheriting from that for each individual piece
    - one class for the board

# TODO and updates: (add updates here after each session)
- moved loadfromfen to piece.py
- need to finish loadfromfen

2022/02/24
- [X] Access squares in load_from_fen
- [X] Assign each square a piece (its occupant) + each piece its square
- [X] Render pieces on the board

Notes: 2022/02/24 (midnight!)
- Moved the pieces content over to board.py for convenience (too many piece.kooft calls)
 + if you want to move them back, please copy over the new class definitions as they have changed drastically
- I have no idea why the black rook behaves so strangely after the transform.scale line (it gets transformed to a much smaller size than intended). 
 + An if/else statement could work as a cheap fix because only the picture is corrupted

# TODO:
- [ ] Design moves for each piece...

2022/02/25 - Shadi, 2 hour session
- fixed all image issues, board is in crisp quality
- at what cost you may ask? had to photoshop external images to a fixed size
- pygame.scale was causing the issues

# next steps:
- [X] clean up the code along with the variables
- [ ] drag and drop a piece

2022/03/04 - Shadi, progress over 3 days with minimum work each day
- implemented showing the legal moves of pawns (without moving)
- plan is to do the same for all other pieces
# next steps:
- [ ] drag and drop a piece
