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
- [ ] Calculation to end of board in piece.py
- [ ] knight moves, bishop moves, queen moves, king moves, rook moves

- [ ] in game.py, implement taking, blocked pieces, en passant, castling, check, checkmate, stalemate

--------------------------------------------------------------------------------------------
2022/03/04 - Shadi
- finished drag implementation
# next steps:
- [ ] finish dropping implementation
--------------------------------------------------------------------------------------------

4/25/2022 - Shadi
git checkout to older git branch where there wasn't hyp or phantom
trying to restructure code, then add in piece moves

4/28/2022 - Roham
- [X] clean up piece.py and remove legal moves (add to board later) - SHADI
- [ ] make the unblocked set of moves for each piece in boards - ROHAM
- [ ] make a function to generate all moves and add them to a dictionary mapped with position of the piece (board class, board.py) - ROHAM
- [ ] make a function to generate all legal moves (board.py) with altering the board state after each move - ROHAM
- [X] make pieces able to move again - SHADI
--------------------------------------------------------------------------------------------
BUGS:
    sliding piece can't move when its pinned, to still stay in pin [X] *fixed by shadi, added line of pin
    add promotion [X] 
    revert and forward move doesn't work
    
