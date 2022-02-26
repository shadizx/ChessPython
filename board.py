import pygame
from copy import copy, deepcopy
import os
import piece

# constants
WIDTH = HEIGHT = 512                         # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game

DIMENSION = WIDTH//8
PIECE_SIZE = int(DIMENSION * 0.9)  # adjust the size of pieces on the board
# BLACK_ROOK_SIZE = int(PIECE_SIZE * 15)  # adjustment for the weird bug concerning the black rook

class Piece:
    # default constructor
    def __init__(self, color, type, file=0, rank=0):
        self.color = color
        self.selected = False  # if piece is selected
        self.hasmoved = False
        self.type = type
        self.img = pygame.image.load("assets/" + color + type + ".png")
        # if ((self.color == 'b') and (self.type == 'r')):
        #     self.img = pygame.transform.scale(self.img, (BLACK_ROOK_SIZE, BLACK_ROOK_SIZE))

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
        offset = (DIMENSION-PIECE_SIZE)//2
        WIN.blit(self.img, ((DIMENSION * self.file + offset - 1), (HEIGHT - DIMENSION * (self.rank + 1) + offset)))

# class piece


# creating specific pieces that inherit from piece class
class pawn(Piece):

    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="p", file=file, rank=rank)  # have to keep it like this for the defaults to work!

        self.type = "p"


class bishop(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="b", file=file, rank=rank)
        self.type = "b"


class knight(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="n", file=file, rank=rank)
        self.type = "n"


class rook(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="r", file=file, rank=rank)
        self.type = "r"


class queen(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="q", file=file, rank=rank)
        self.type = "q"


class king(Piece):
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="k", file=file, rank=rank)
        self.type = "k"

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
        pygame.draw.rect(WIN, self.color, pygame.Rect((DIMENSION*(self.file)), (HEIGHT-DIMENSION*(self.rank+1)), DIMENSION, DIMENSION))
        # if self.occupant is not None:
        #     pygame.blit()  # TODO finish this with occupant class's png and position of the piece on board + a certain number of squares

    
# store default values used for board translation here!
StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
PIECES_DICT = {'p': pawn("b"),   'n': knight("b"),
                'b': bishop("b"), 'r': rook("b"),
                'q': queen("b"),  'k': king("b"),
                'P': pawn("w"),   'N': knight("w"),
                'B': bishop("w"), 'R': rook("w"),
                'Q': queen("w"),  'K': king("w")}
FILELIST = ["a","b","c","d","e","f","g","h"]
RANKLIST = [1,2,3,4,5,6,7,8]
TURNDICT = {'w': 0, 'b': 1}  # TODO: edit this as required!
CASTLINGDICT = {'k': "black_kingside", 'K': "white_kingside", 'q': "black_queenside", 'Q': "white_queenside"}  # TODO: edit this!
STARTPIECES = []  # might want to set up the entire starting position pieces into this if you want to avoid initializing board from FEN

class Board:
    SquareDict = {}
    Pieces = []
    Turn = 'w'  # placeholder for further editing, if functionality is needed by game.py
    CastlingsAllowed = [CASTLINGDICT[i] for i in CASTLINGDICT]  # starting board has all castles allowed
    EnPassantSquare = None
    MovesSinceLastPawn = 0
    MoveNumber = 1

    def __init__(self, FEN=StartFEN):
        for indexf, l in enumerate(FILELIST):
            for indexr, n in enumerate(RANKLIST):
                isWhite = (indexf + indexr) % 2 != 0
                temp = Square(indexf, indexr, isWhite)
                self.SquareDict[(l, n)] = temp
        self.FEN = FEN

    def LoadFromFEN(self):
        self.CastlingsAllowed = []  # resets castles so we can assign them again here
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
                piece = copy(PIECES_DICT[s])  # IMPORTANT: generate a COPY of the object to avoid overwrite issues!
                piece.setpos(file, rank)
                self.Pieces.append(piece)
                self.SquareDict[(FILELIST[file], RANKLIST[rank])].Occupant = PIECES_DICT[s]
                file += 1
        for s in splitfen[1]:  # Toggle turns
            self.Turn = 'w' if s == 'w' else 'b'
        for s in splitfen[2]:  # Toggle castling states
            if s in CASTLINGDICT:
                self.CastlingsAllowed.append(CASTLINGDICT[s])
        if splitfen[3] != '-':  # Translate en passant square to a square on the board, if available
            s = splitfen[3]
            self.EnPassantSquare = self.SquareDict[(s[0], s[1])]
        self.MovesSinceLastPawn = int(splitfen[4])  # determine moves since last pawn move (for 50-move rule)
        self.MoveNumber = int(splitfen[5])  # determine move number

    def drawboard(self):
        for square in self.SquareDict.values():
            square.draw()
        for p in self.Pieces:
            # print([p.file, p.rank]) # testing
            p.draw()


# function needed for refreshing window
def drawboard():
    mainboard = Board()
    mainboard.drawboard()
    pygame.display.update()



def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    mainboard = Board()
    mainboard.LoadFromFEN()
    mainboard.drawboard()
    # img = pygame.image.load("assets/pieces/wk.svg")
    # WIN.blit(img, (200, 300))
    pygame.display.update()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main()