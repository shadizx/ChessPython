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

############################################################   
# Class piece -------------------------------------------
# general parent class for each piece, is inherited from for efficient code
class Piece:
    # default constructor
    def __init__(self, color, type, position = 0):
        self.color = color
        self.selected = False  # if piece is selected
        self.hasmoved = False
        self.type = type
        self.img = pygame.image.load("assets/" + color + type + ".png")
        self.rect = self.img.get_rect()
        self.clicked = False
        self.moves = []
        self.position = position
    #################################################
    def setPos(self, position):  # easy navigation
        self.position = position
    #############################################3
    # checking if a piece is selected
    def isSelected(self):
        return self.selected

    # printing a piece on the board, centralized on their respective squares:
    def draw(self):
        xloc = (self.position % 8)
        yloc = ((self.position - xloc)/8)
        # print(self.color + " " + self.type + " at position (" + str(xloc) + ", " + str(yloc) + ")")
        win.blit(self.img, ((xloc * dimension), height - dimension -  yloc * dimension))
# Class piece ---------------------------------------------

# creating specific pieces that inherit from piece class
# class pawn(piece) ---------------------------------------
class pawn(Piece):
    CanTakeLeft = False
    CanTakeRight = False
    def __init__(self, color, position = 0):
        super().__init__(color, type="p")  # have to keep it like this for the defaults to work!
        self.type = "p"
    def legalmoves(self):
        self.moves = []
        # if king will not be in check after piece moves
        #   if there is no piece in way of the current piece
        #       then move the piece

        # grab the file of the piece
        # if piece is black:
        if self.color == "b":
            self.moves.append(self.position - 8)
            self.moves.append(self.position - 16)
            # if self.rank == 6:
            #     self.moves.append((self.position, self.rank - 2))
            # if self.CanTakeLeft:
            #     self.moves.append((l-1, self.rank - 1))
            # if self.CanTakeRight:
            #     self.moves.append((l+1, self.rank - 1))
        else:
            self.moves.append(self.position + 8)
            self.moves.append(self.position + 16)
            # if self.rank == 1:
            #     self.moves.append((self.file, self.rank + 2))
            # if self.CanTakeLeft:
            #     self.moves.append((l-1, self.rank + 1))
            # if self.CanTakeRight:
            #     self.moves.append((l+1, self.rank + 1))

        # print(f"my legal moves are {self.moves}")

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
# class king(piece) -------------------------------------------