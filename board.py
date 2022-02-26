import pygame
from copy import copy, deepcopy
import os
import piece

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
###################### constants ############################

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

###################################################################
# class Square:
# responsible for each square on the board
class Square:
    # default constructor
    WHITE=(248,220,180)
    BLACK=(184,140,100)
    Occupant = None

    def __init__(self, file, rank, color, occupant = None):
        self.file = file
        self.rank = rank
        self.isWhite = color
        self.color = self.WHITE if self.isWhite else self.BLACK
        self.Occupant = occupant

    #occupant:piece.Piece = None

    def draw(self):
        pygame.draw.rect(win, self.color, pygame.Rect((dimension*(self.file)), (height-dimension*(self.rank+1)), dimension, dimension))
        # if self.occupant is not None:
        #     pygame.blit()  # TODO finish this with occupant class's png and position of the piece on board + a certain number of squares

# class square
###################################################################

###################################################################
# class fen
# store default values used for board translation
class fen():
    # public values to be accessed later on
    PIECES_DICT = {'p': pawn("b"),   'n': knight("b"),
                'b': bishop("b"), 'r': rook("b"),
                'q': queen("b"),  'k': king("b"),
                'P': pawn("w"),   'N': knight("w"),
                'B': bishop("w"), 'R': rook("w"),
                'Q': queen("w"),  'K': king("w")}
    FILELIST = ["a","b","c","d","e","f","g","h"]
    RANKLIST = [1,2,3,4,5,6,7,8]
    castling_dict = {'k': "black_kingside", 'K': "white_kingside", 'q': "black_queenside", 'Q': "white_queenside"}  # TODO: edit this!
    StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    CastlingsAllowed = []  # resets castles so we can assign them again here
    turn_dict = {'w': 0, 'b': 1}  # TODO: edit this as required!
    STARTPIECES = []  # might want to set up the entire starting position pieces into this if you want to avoid initializing board from FEN
    # LoadfromFEN
    # load the board from a FEN
    def LoadFromFEN(self):
        splitfen = self.FEN.split(' ')
        file = 0
        rank = 7
        for s in splitfen[0]:  # Loop through the first string: piece placement
            if s == "/":
                rank -= 1
                file = 0
            elif s in ['1', '2', '3', '4', '5', '6', '7', '8']:
                file += int(s)
            else:
                piece = copy(self.PIECES_DICT[s])  # IMPORTANT: generate a COPY of the object to avoid overwrite issues!
                piece.setpos(file, rank)
                self.Pieces.append(piece)
                self.SquareDict[(self.FILELIST[file], self.RANKLIST[rank])].Occupant = self.PIECES_DICT[s]
                file += 1
        for s in splitfen[1]:  # Toggle turns
            self.Turn = 'w' if s == 'w' else 'b'
        for s in splitfen[2]:  # Toggle castling states
            if s in self.castling_dict:
                self.CastlingsAllowed.append(self.castling_dict[s])
        if splitfen[3] != '-':  # Translate en passant square to a square on the board, if available
            s = splitfen[3]
            self.EnPassantSquare = self.SquareDict[(s[0], s[1])]
        self.MovesSinceLastPawn = int(splitfen[4])  # determine moves since last pawn move (for 50-move rule)
        self.MoveNumber = int(splitfen[5])  # determine move number
# class fen
###################################################################

###################################################################
# class Board
# inherits from fen, responsible for structure of board
class Board(fen):

    SquareDict = {}
    Pieces = []
    Turn = 'w'  # placeholder for further editing, if functionality is needed by game.py
    EnPassantSquare = None
    MovesSinceLastPawn = 0
    MoveNumber = 1

    def __init__(self):
        CastlingsAllowed = [self.castling_dict[i] for i in self.castling_dict]  # starting board has all castles allowed
        for indexf, l in enumerate(self.FILELIST):
            for indexr, n in enumerate(self.RANKLIST):
                isWhite = (indexf + indexr) % 2 != 0
                temp = Square(indexf, indexr, isWhite)
                self.SquareDict[(l, n)] = temp
        self.FEN = self.StartFEN

#class board
###################################################################
# drawboard()
# useful for drawing the board
def drawboard():
    squareimgs = Board()
    for square in squareimgs.SquareDict.values():
        square.draw()
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    pieceimgs = Board()
    for p in pieceimgs.Pieces:
        p.draw()
###################################################################

# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    mainboard = Board()
    mainboard.LoadFromFEN()
    drawboard()
    drawpieces()
    
    pygame.display.update()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main()