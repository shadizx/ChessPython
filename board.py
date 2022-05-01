
# board.py
# responsible for boad structure and operations
import pygame
from copy import copy
import piece
from dataclasses import dataclass
from collections import defaultdict

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
DEFAULTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
###################### global variables ############################

##############################################################
# class fen
# store default values used for board translation

@dataclass# returns piecelist array
class fen():
    # public values to be accessed later on
    FEN: str
    PIECES_DICT = {'p': piece.pawn("b"),   'n': piece.knight("b"),
                   'b': piece.bishop("b"), 'r': piece.rook("b"),
                   'q': piece.queen("b"),  'k': piece.king("b"),
                   'P': piece.pawn("w"),   'N': piece.knight("w"),
                   'B': piece.bishop("w"), 'R': piece.rook("w"),
                   'Q': piece.queen("w"),  'K': piece.king("w")}
    castling_dict = {'k': "black_kingside", 'K': "white_kingside", 'q': "black_queenside", 'Q': "white_queenside"}  # TODO: edit this!
    # StartFEN = DEFAULTFEN
    CastlingsAllowed = []  # resets castles so we can assign them again here
    turn_dict = {'w': 0, 'b': 1}  # TODO: edit this as required!

    # assigning pieceList array
    pieces = {}
    # LoadfromFEN
    # load the board from a FEN
    def LoadFromFEN(self):
        self.EnPassantSquare = -1
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
                piece.setPos(position)
                self.pieces[position] = piece
                file += 1
        for s in splitfen[1]:  # Toggle turns
            self.Turn = 'w' if s == 'w' else 'b'
        for s in splitfen[2]:  # Toggle castling states
            if s in self.castling_dict:
                self.CastlingsAllowed.append(self.castling_dict[s])
        if splitfen[3] != '-':  # Translate en passant square to a square on the board, if available
            s = splitfen[3]
            self.EnPassantSquare = 0
            # self.EnPassantSquare = self.SquareDict[(s[0], s[1])]  # TODO: fix this!
        self.MovesSinceLastPawn = int(splitfen[4])  # determine moves since last pawn move (for 50-move rule)
        self.MoveNumber = int(splitfen[5])  # determine move number

        return (self.pieces, self.Turn, self.CastlingsAllowed, self.EnPassantSquare, self.MovesSinceLastPawn, self.MoveNumber)

# class fen
###################################################################

###################################################################
# class Square:
# responsible for each square on the board
class Square:
    # default constructor
    WHITE=(248,220,180)
    BLACK=(184,140,100)

    def __init__(self, position, color):
        self.position = position
        self.isWhite = color
        self.color = self.WHITE if self.isWhite else self.BLACK

    def draw(self):
        y, x = divmod(self.position, 8)
        pygame.draw.rect(win, self.color, pygame.Rect(x * dimension, height - (y+1) * dimension, dimension, dimension))

# class square
###################################################################

###################################################################
# class Board
# inherits from fen, responsible for board square colors
class Board:

    # holds boardcolors
    boardColors = []
    # dict that maps a position to the legal moves of the piece on that position
    moveDict = defaultdict(lambda: [])
    # list of moves that has happened so far:
    moveList = []
    # start with this FEN
    FEN = DEFAULTFEN
    # tracks taken pieces to use in revertmove
    # maps the move number to a piece that was taken on that move
    takenPieces = {}
    # tracks number of moves that have been played
    moveCounter = 0


    enpassantPawnPos = -1

    def __init__(self):
        self.pieceList, self.turn, self.castlingsAllowed, self.enpassantSquare, self.movesSinceLastPawn, self.moveNumber = fen(self.FEN).LoadFromFEN()
        self.generateMoves()


    # generateMoves
    # useful for generating the moves of board
    def generateMoves(self):
        # clear the moveDict
        self.moveDict.clear()
        for piece in self.pieceList.values():
            if piece.type == 'p':
                self.loadpmoves(piece)
            elif piece.type == "r":
                self.loadrmoves(piece)
            elif piece.type == "n":
                self.loadnmoves(piece)
            elif piece.type == "b":
                self.loadbmoves(piece)
            elif piece.type == "q":
                self.loadqmoves(piece)
            elif piece.type == "k":
                self.loadkmoves(piece)


    # loadpmoves
    # loads pawn moves for all pawns
    def loadpmoves(self, pawn):
        # take pawn position into pos for ease of use
        pos = pawn.position
        # assign col to -1 or 1 to make it easier to calculate legal moves for w or b pawn
        if pawn.color == "w": 
            col = 1
        else: 
            col = -1
        #######################################################################
        # first lets calculate just moving the pawn:
        # if the position in front of the pawn is empty
        if pos + 8 * col not in self.pieceList:
            self.moveDict[pos].append(pos + 8 * col)

            # if on first move then add the extra 2 spaced move
            # if white and on 2nd rank, or black and on 7th rank
            if (pos // 8 == 1 and col == 1) or (pos // 8 == 6 and col == -1):
                if pos + 16 * col not in self.pieceList:
                    self.moveDict[pos].append(pos + 16 * col)
        #######################################################################
        # now lets calculate taking a piece
        # check if there is a pawn diagonal from the current pawn and opposite color
        for takePos in [pos + 9 * col, pos + 7 * col]:
            if takePos in self.pieceList and self.pieceList[takePos].color != pawn.color:
                # need to add an extra check for pawns on the edge of the board
                # check if file of the takePos is way different than file of pos
                if abs((takePos % 8) - (pos % 8)) == 1:
                    self.moveDict[pos].append(takePos)
        #######################################################################
        # calculating en passant moves:
        # parameters for an en passant move is:
        #   1) if previous move was a pawn move played to the exact right or left of a pawn
        #   2) and this happens on rank 5 (for white) and rank 4 (for black)

        # check if there has been a move played
        if len(self.moveList) != 0:
            # get coordinates of the other peice's position (last position and current one)
            otherPiecePos = (self.moveList[-1])[1]
            otherPiecePrevPos = (self.moveList)[-1][0]
            # get rank and file from otherPiecePos
            otherPieceRank, otherPieceFile = piece.getRankFile(otherPiecePos)
            otherPiecePrevRank, otherPiecePrevFile = piece.getRankFile(otherPiecePrevPos)
            # get the current rank and file
            currRank, currFile = piece.getRankFile(pos)

            if (    
                    # check if last move was a pawn move of opposite color
                    (otherPiecePos in self.pieceList) and 
                    (self.pieceList[otherPiecePos].type == "p") and 
                    (self.pieceList[otherPiecePos].color != pawn.color) and
                    # check if last move is a pawn move that went 2 squares up
                    (abs(otherPiecePrevPos - otherPiecePos) == 16) and
                    # check if on same rank and left/right file
                    ((abs(otherPieceFile - currFile) == 1)) and
                    (otherPieceRank == currRank) and 
                    (abs(pos - otherPiecePos) == 1) and
                    # check if this happens on rank 5 (for white) and rank 4 (for black):
                    ((pos // 8 == 4 and pawn.color == "w") or (pos // 8 == 3 and pawn.color == "b"))
            ):
                self.moveDict[pos].append(otherPiecePos + 8 * col)
                self.enpassantPawnPos = otherPiecePos
                print("EN CHOSSANT")                

    # loadnmoves
    # loads knight moves for all knights
    def loadnmoves(self, piece):
        pass

    # loadrmoves
    # loads rook moves for all rooks
    def loadrmoves(self, piece):
        pass

    # loadbmoves
    # loads bishop moves for all bishops
    def loadbmoves(self, piece):
        pass

    # loadqmoves
    # loads queen moves for all queens
    def loadqmoves(self, piece):
        pass

    # loadkmoves
    # loads king moves for all kings
    def loadkmoves(self, piece):
        pass

    # makeMove
    # useful for moving a piece and updating our directory accordingly
    def makeMove(self, origin, dest):
        self.moveCounter += 1
        print("on move", self.moveCounter)

        # grab the piece, move it to the destination
        piece = self.pieceList[origin]

        # get color of piece
        col = 1 if piece.color == "w" else -1

        # if there is a piece being taken track that
        if dest in self.pieceList:
            self.takenPieces[self.moveCounter] = self.pieceList[dest]
            print("TAKEN PIECE ON MOVE", self.moveCounter)

        if self.turn == piece.color:
            # delete en passant'ed pawn if needed
            # need to check if the enpassant is ACTUALLY done
            if piece.type == "p" and ((dest - self.enpassantPawnPos) == 8 * col):
                self.takenPieces[self.moveCounter] = self.pieceList[self.enpassantPawnPos]
                del self.pieceList[self.enpassantPawnPos]
                self.enpassantPawnPos = -1
                print("EN CHOSSANT HAS BEEN TAKEN")

            # move the piece to its destination
            piece.setPos(dest)
            # update the position of the piece in pieceList
            self.pieceList[dest] = self.pieceList.pop(origin)  # YES, this also deletes the piece in origin
            # add the move to moveList
            self.moveList.append((origin, dest))

            # check how many moves since last pawn move
            if piece.type != 'p':
                self.MovesSinceLastPawn += 1 if self.turn == 'b' else 0
            else:
                self.MovesSinceLastPawn = 0
            self.turn = 'w' if self.turn == 'b' else 'b'

            print("move list is " + str(self.moveList))
            # TODO: also update CastlingsAllowed AND enpassant square right here (much neater)

    def revertMove(self):
        if self.moveCounter != 0:
            previousOrigin, previousDest = (self.moveList.pop(-1))  # removes and returns the last element
            # grab the piece, move it back to the origin
            # revert the piece that just moved
            self.pieceList[previousOrigin] = self.pieceList.pop(previousDest)
            self.pieceList[previousOrigin].setPos(previousOrigin)
            # see if there was a piece taken on previous dest
            if self.moveCounter in self.takenPieces:
                takenPiece = self.takenPieces.pop(self.moveCounter)
                self.pieceList[takenPiece.position] = takenPiece
            self.moveCounter -= 1
            self.turn = 'w' if self.turn == 'b' else 'b'
            # TODO: find a way to revert changes to castle and enpassant square and moves since last pawn
    # draw
    # draws board squares
    def draw(self):
        # first time draw is called, load the square
        # next time, just draw the squares
        if len(self.boardColors) == 0:
            for position in range(64):
                isWhite = sum(piece.getRankFile(position)) % 2 != 0
                temp = Square(position, isWhite)
                temp.draw()
                self.boardColors.append(temp)
        else:
            for square in self.boardColors:
                square.draw()

#class board
###################################################################