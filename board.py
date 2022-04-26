# board.py
# responsible for boad structure and operations
import pygame
from copy import copy, deepcopy
import piece

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
DEFAULTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
###################### constants ############################

##############################################################
# class fen
# store default values used for board translation
# returns piecelist array
class fen():
    # public values to be accessed later on
    PIECES_DICT = {'p': piece.pawn("b"),   'n': piece.knight("b"),
                   'b': piece.bishop("b"), 'r': piece.rook("b"),
                   'q': piece.queen("b"),  'k': piece.king("b"),
                   'P': piece.pawn("w"),   'N': piece.knight("w"),
                   'B': piece.bishop("w"), 'R': piece.rook("w"),
                   'Q': piece.queen("w"),  'K': piece.king("w")}
    FILELIST = ["a","b","c","d","e","f","g","h"]
    RANKLIST = [1,2,3,4,5,6,7,8]
    castling_dict = {'k': "black_kingside", 'K': "white_kingside", 'q': "black_queenside", 'Q': "white_queenside"}  # TODO: edit this!
    StartFEN = DEFAULTFEN
    CastlingsAllowed = []  # resets castles so we can assign them again here
    turn_dict = {'w': 0, 'b': 1}  # TODO: edit this as required!

    # assigning pieceList array
    pieceList = [None] * 64
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
                # set piece position according to formula below
                position = 8 * rank + file

                piece = copy(self.PIECES_DICT[s])  # IMPORTANT: generate a COPY of the object to avoid overwrite issues!
                piece.setpos(position)
                self.pieceList[position] = piece
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

        return self.pieceList

# class fen
###################################################################

###################################################################
# class Square:
# responsible for each square on the board
class Square:
    # default constructor
    WHITE=(248,220,180)
    BLACK=(184,140,100)

    def __init__(self, file, rank, color):
        self.file = file
        self.rank = rank
        self.isWhite = color
        self.color = self.WHITE if self.isWhite else self.BLACK

    def draw(self):
        pygame.draw.rect(win, self.color, pygame.Rect((dimension*(self.file)), (height-dimension*(self.rank+1)), dimension, dimension))

# class square
###################################################################

###################################################################
# class Board
# inherits from fen, responsible for structure of board
class Board(fen):

    boardColors = {}
    Pieces = []
    Turn = 'w' # placeholder for further editing, if functionality is needed by game.py
    EnPassantSquare = None
    MovesSinceLastPawn = 0
    MoveNumber = 1

    def __init__(self):
        for indexf, l in enumerate(self.FILELIST):
            for indexr, n in enumerate(self.RANKLIST):
                isWhite = (indexf + indexr) % 2 != 0
                temp = Square(indexf, indexr, isWhite)
                self.boardColors[(l, n)] = temp
        self.FEN = self.StartFEN

#class board
###################################################################