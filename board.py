# board.py
# responsible for boad structure and operations

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
DEFAULTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
###################### constants ############################

PIECESloc = {'a1': None, 'b1': None, 'c1': None, 'd1': None, 'e1': None, 'f1': None, 'g1': None, 'h1': None,
             'a2': None, 'b2': None, 'c2': None, 'd2': None, 'e2': None, 'f2': None, 'g2': None, 'h2': None,
             'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
             'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
             'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
             'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
             'a7': None, 'b7': None, 'c7': None, 'd7': None, 'e7': None, 'f7': None, 'g7': None, 'h7': None,
             'a8': None, 'b8': None, 'c8': None, 'd8': None, 'e8': None, 'f8': None, 'g8': None, 'h8': None}

###################################################################
# class fen
# store default values used for board translation
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
    StartFEN = "rnbqkbnr/pppppppp/8/8/6p1/6P1/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
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
                PIECESloc[(self.FILELIST[file] + str(self.RANKLIST[rank]))] = piece
                # print(piece.type + "ON SQUARE [" + str(piece.file) + ", " + str(piece.rank) + "]")
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