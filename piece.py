import pygame

# general piece class for all pieces
class piece:
    # default constructor
    def __init__(self, row, col, color, type, val): 
        self.row = row
        self.col = col
        self.color = color
        self.type = ""        # type of piece (string, ex: bishop, etc..)
        self.val = 0          # value of the piece
        self.selected = False # if piece is selected
    
    # moving a piece
    def move(self):
        pass

    # checking if a piece is selected
    def isSelected(self):
        return self.selected
    
    # printing a piece on the board
    def draw(self):
        pass
# class piece

# creating specific pieces that inherit from piece class

class pawn(piece):
    pass

class bishop(piece):
    pass

class knight(piece):
    pass

class rook(piece):
    pass

class queen(piece):
    pass

class king(piece):
    pass