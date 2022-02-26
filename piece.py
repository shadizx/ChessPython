# piece.py
# responsible for functionality of the pieces

import pygame
import os

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
###################### constants ###########################             

# Class piece -------------------------------------------
# general parent class for each piece, is inherited from for efficient code
class Piece:
    # default constructor
    def __init__(self, color, type, file=0, rank=0):
        self.color = color
        self.selected = False  # if piece is selected
        self.hasmoved = False
        self.type = type
        self.img = pygame.image.load("assets/" + color + type + ".png")

    def setpos(self, file, rank):  # easy navigation
        self.file = file
        self.rank = rank

    # moving a piece
    def move(self):
        pass

    # checking if a piece is selected
    def isSelected(self):
        return self.selected

    # printing a piece on the board, centralized on their respective squares:
    def draw(self):
        offset = (dimension-piece_size)//2
        win.blit(self.img, ((dimension * self.file + offset - 3), (height - dimension * (self.rank + 1) + offset - 3)))
# Class piece ---------------------------------------------

# creating specific pieces that inherit from piece class
# class pawn(piece) ---------------------------------------
class pawn(Piece):

    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="p", file=file, rank=rank)  # have to keep it like this for the defaults to work!

        self.type = "p"
# class pawn(piece) ----------------------------------------

# class bishop(piece) --------------------------------------
class bishop(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="b", file=file, rank=rank)
        self.type = "b"
# class bishop(piece) --------------------------------------

# class knight(piece) --------------------------------------
class knight(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="n", file=file, rank=rank)
        self.type = "n"
# class knight(piece) --------------------------------------

# class rook(piece) ----------------------------------------
class rook(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="r", file=file, rank=rank)
        self.type = "r"
# class rook(piece) -----------------------------------------

# class queen(piece) ----------------------------------------
class queen(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="q", file=file, rank=rank)
        self.type = "q"
# class queen(piece) -----------------------------------------

# class king(piece) ------------------------------------------
class king(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="k", file=file, rank=rank)
        self.type = "k"
# class king(piece) -------------------------------------------