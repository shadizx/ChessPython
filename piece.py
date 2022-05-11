# piece.py
# responsible for functionality of the pieces
import pygame
###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
###################### constants ###########################      
getRankFile = lambda position: divmod(position, 8)
getPos = lambda y, x: y*8+x
############################################################   
# Class piece -------------------------------------------
# general parent class for each piece, is inherited from for efficient code
class Piece:
    # default constructor
    def __init__(self, color, type, position = 0):
        self.color = color
        self.type = type
        self.position = position
        self.img = pygame.image.load("assets/" + color + type + ".png")
    #################################################
    def setPos(self, position):  # easy navigation
        self.position = position
    #############################################3
    # printing a piece on the board, centralized on their respective squares:
    def draw(self):
        yloc, xloc = divmod(self.position, 8)
        win.blit(self.img, ((xloc * dimension), height - dimension -  yloc * dimension))
# Class piece ---------------------------------------------

# creating specific pieces that inherit from piece class
# class pawn(piece) ---------------------------------------
class pawn(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="p")  # have to keep it like this for the defaults to work!
        self.type = "p"
# class pawn(piece) ----------------------------------------

# class bishop(piece) --------------------------------------
class bishop(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="b")
        self.type = "b"
# class bishop(piece) --------------------------------------

# class knight(piece) --------------------------------------
class knight(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="n")
        self.type = "n"
# class knight(piece) --------------------------------------

# class rook(piece) ----------------------------------------
class rook(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="r")
        self.type = "r"
        self.hasMoved = False
# class rook(piece) -----------------------------------------

# class queen(piece) ----------------------------------------
class queen(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="q")
        self.type = "q"
# class queen(piece) -----------------------------------------

# class king(piece) ------------------------------------------
class king(Piece):
    def __init__(self, color, position = 0):
        super().__init__(color, type="k")
        self.type = "k"
        self.hasMoved = False
# class king(piece) -------------------------------------------