# board.py
# responsible for boad structure and operations
import pygame
from copy import copy
import piece
from dataclasses import dataclass
from collections import defaultdict

###################### aconstants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
DEFAULTFEN = "4k/n/6rp//6N/R4P//5K w KQkq - 0 1"
###################### global variables ############################

##############################################################

###################################################################
# class Board
# inherits from fen, responsible for board square colors
class Board:

    # holds boardcolors
    boardColors = []
    # dict that maps a piece to the legal moves of that piece
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
    # tracks unmade moves to then go forward with arrow key
    unmadeMoves = []
    # to check if enpassant is available
    enpassantPawnPos = -1
    # dictionary that maps a position that a piece(s) can go to, to the pieces that can go there
    # format: {43, [p,k,r]}
    # this means that the pawn king and rook can all go to square 43
    checkDict = defaultdict(lambda: [])
    # dict that tracks the kings position
    # format: {"w" : 4, "b" : 60} means white king is on square 4 and black is on 60
    kings = {"w" : 4, "b" : 60}
    # line of check set
    # set that contains the line of check (positions)
    lineOfCheck = set()
    # incheck boolean set to check if king is in check
    inCheck = False
    # two dicts for legal moves of white and black
    whiteLegalMoves = defaultdict(lambda: [])
    blackLegalMoves = defaultdict(lambda: [])

    def __init__(self):
        self.pieceList, self.turn, self.castlingsAllowed, self.enpassantSquare, self.movesSinceLastPawn, self.moveNumber = fen(self.FEN).LoadFromFEN()
        self.generateMoves(self.turn)

    # generateMoves
    # useful for generating the moves of board
    def generateMoves(self, turn):
        # clear the moveDict
        for piece in self.pieceList.values():
            if piece.color == turn:
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

    # adds move to both moveDict and checkdict
    def addMove(self, piece, dest):
        self.moveDict[piece].append(dest)
        if dest in self.pieceList:
            self.checkDict[dest].append(piece)
        if piece.color == "w":
            self.whiteLegalMoves[dest].append(piece)
        else:
            self.blackLegalMoves[dest].append(piece)

    # function for checking if king is in check in O(1) time
    # updates the line of check set efficiently 
    def isInCheck(self, color):
        # check if position of the king is in the legal moves
        # if it is, it updates the line of check

        # get kings position
        kingPos = self.kings[color]
        kingRank, kingFile = piece.getRankFile(kingPos)
        # if the king is in check

        # print("move number is", self.moveCounter, "king pos is ", kingPos, "check dict is ", str(self.checkDict))
        if kingPos in self.checkDict:
            print(color, "is in check")
            self.inCheck = True
            # loop through each line of check (max 2, usually 1)
            for i in range(len(self.checkDict[kingPos])):
                # get the piece that's attacking
                oppPiece = self.checkDict[kingPos][i]
                oppPos = oppPiece.position
                oppRank, oppFile = piece.getRankFile(oppPiece.position)
                if oppPiece.type in ("p", "n"):
                    # if pawn or knight is attacking, you can only take the pawn
                    # therefore line of check is just the piece's position
                    self.lineOfCheck.add(oppPiece.position)
                elif oppPiece.type in ("b", "q"):
                    # if bishop is attacking, we need all the diagonal squares
                    # if king is northeast of bishop
                    if (kingRank > oppRank and kingFile > oppFile):
                        for pos in range(oppPos, kingPos, 9):
                            self.lineOfCheck.add(pos)
                    # if king is southeast of bishop
                    elif (kingRank < oppRank and kingFile > oppFile):
                        for pos in range(oppPos, kingPos, -7):
                            self.lineOfCheck.add(pos)
                    # if king is southwest of bishop
                    elif (kingRank < oppRank and kingFile < oppFile):
                        for pos in range(oppPos, kingPos, -9):
                            self.lineOfCheck.add(pos)
                    # if king is northwest of bishop
                    elif (kingRank > oppRank and kingFile < oppFile):
                        for pos in range(oppPos, kingPos, 7):
                            self.lineOfCheck.add(pos)
                elif oppPiece.type in ("r","q"):
                    # if rook or queen is attacking, need vertical and horz squares
                    # if king is to the right of attacking piece:
                    if (kingRank == oppRank and kingFile > oppFile):
                        for pos in range(oppPos, kingPos, 1):
                            self.lineOfCheck.add(pos)
                    # if king is to the left of attacking piece:
                    elif (kingRank == oppRank and kingFile < oppFile):
                        for pos in range(oppPos, kingPos, -1):
                            self.lineOfCheck.add(pos)
                    # if king is above attacking piece:
                    elif (kingRank > oppRank and kingFile == oppFile):
                        for pos in range(oppPos, kingPos, 8):
                            self.lineOfCheck.add(pos)
                    # if king is below attacking piece:
                    elif (kingRank < oppRank and kingFile == oppFile):
                        for pos in range(oppPos, kingPos, -8):
                            self.lineOfCheck.add(pos)
        else:
            self.inCheck = False

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
            # if king is in check, only add move if it blocks line of check
            if ((self.inCheck and (pos + 8 * col in self.lineOfCheck)) or (not self.inCheck)):
                self.moveDict[pawn].append(pos + 8 * col)

            # if on first move then add the extra 2 spaced move
            # if white and on 2nd rank, or black and on 7th rank
            if pos + 16 * col not in self.pieceList and ((pos // 8 == 1 and col == 1) or (pos // 8 == 6 and col == -1)):
                if ((self.inCheck and (pos + 16 * col in self.lineOfCheck)) or (not self.inCheck)):
                    self.moveDict[pawn].append(pos + 16 * col)
        #######################################################################
        # now lets calculate taking a piece
        # check if there is a pawn diagonal from the current pawn and opposite color
        for takePos in [pos + 9 * col, pos + 7 * col]:
            if takePos in self.pieceList and self.pieceList[takePos].color != pawn.color:
                # need to add an extra check for pawns on the edge of the board
                # check if file of the takePos is way different than file of pos
                if abs((takePos % 8) - (pos % 8)) == 1:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(pawn, takePos)
            elif takePos not in self.pieceList:
                self.whiteLegalMoves[takePos].append(pawn) if pawn.color == "w" else self.blackLegalMoves[takePos].append(pawn)
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
            # otherPiecePrevRank, otherPiecePrevFile = piece.getRankFile(otherPiecePrevPos)
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
                    (abs(pos - otherPiecePos) == 1)
                    # check if this happens on rank 5 (for white) and rank 4 (for black):
                    # ((pos // 8 == 4 and pawn.color == "w") or (pos // 8 == 3 and pawn.color == "b"))
            ):
                if ((self.inCheck and (otherPiecePos + 8 * col in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(pawn, otherPiecePos + 8 * col)
                    self.enpassantPawnPos = otherPiecePos
                    print("EN CHOSSANT")

    # loadnmoves
    # loads knight moves for all knights
    def loadnmoves(self, knight):
        pos = knight.position

        # take the file of our knight for restrictions
        fileOrigin = pos % 8
        # +-15, +-17, +-6, +-10 are the legal possible moves for knight
        for takePos in [pos + 15, pos + 17, pos + 6, pos + 10, pos - 15, pos - 17, pos - 6, pos - 10]:
            # take file of opp knight to compare below
            file = takePos % 8
            # difference of files must be 1 or 2 to be a valid knight move
            if ((abs(fileOrigin - file) in [1,2]) and (0 <= takePos <= 64)):
                # check if piece exists there with a different color
                if (takePos in self.pieceList):
                    if (self.pieceList[takePos].color != knight.color):
                        if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                            self.addMove(knight, takePos)
                else:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(knight, takePos)

    # loadrmoves
    # loads rook moves for all rooks
    def loadrmoves(self, rook):
        pos = rook.position
        rank,file = piece.getRankFile(pos)
        # first calculate north moves:
        for takePos in range(pos + 8, 64, 8):
            # check if there is a piece on a square
            if takePos in self.pieceList:
                # check if opp color, then append that move and go to the next one
                if self.pieceList[takePos].color != rook.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(rook, takePos)
                        break
                else:
                    # if same color on that square, then break
                    break
            else:
                # if no piece on that square, append move and keep going
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(rook, takePos)

        # calculate south moves:
        for takePos in range(pos - 8, file - 1, -8):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != rook.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(rook, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(rook, takePos)

        # calculate east moves:
        for takePos in range(pos + 1, 8 * (rank + 1) , +1):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != rook.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(rook, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(rook, takePos)

        # #calculate west moves:
        for takePos in range(pos - 1, 8 * rank - 1, -1):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != rook.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(rook, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(rook, takePos)

    # loadbmoves
    # loads bishop moves for all bishops
    def loadbmoves(self, bishop):
        pos = bishop.position
        rankOrigin,fileOrigin = piece.getRankFile(pos)
        # first calculate up right moves:
        # each time you go up right, file increases by one AND rank
        # therefore, the max you can go to the up right direction is 
        #   (7 - (max of file and rank)) spaces up right
        #   up right is 9 spaces, therefore formula is 
        lim = (7 - max(rankOrigin, fileOrigin)) * 9 + pos
        for takePos in range(pos + 9, lim + 1, 9):
            # check if there is a piece on a square
            if takePos in self.pieceList:
                # check if opp color, then append that move and go to the next one
                if self.pieceList[takePos].color != bishop.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(bishop, takePos)
                        break
                else:
                    # if same color on that square, then break
                    break
            else:
                # if no piece on that square, append move and keep going
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                    self.addMove(bishop, takePos)

        # calculate up left moves:
        # same formula as before, but file decrease by one, also going up 7
        lim = min(fileOrigin, 7 - rankOrigin) * 7 + pos
        for takePos in range(pos + 7, lim + 1, 7):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != bishop.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(bishop, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)): 
                    self.addMove(bishop, takePos)

        #calculate down right moves:
        # similar formula for up left, but rank decreases by one instead of file
        lim = pos - min(7 - fileOrigin, rankOrigin) * 7
        for takePos in range(pos - 7, lim - 1, -7):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != bishop.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(bishop, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)): 
                    self.addMove(bishop, takePos)

        # calculate down left moves:
        # same as up right, but file and rank are both decreasing
        lim = pos - min(rankOrigin, fileOrigin) * 9
        for takePos in range(pos - 9, lim - 1, -9):
            if takePos in self.pieceList:
                if self.pieceList[takePos].color != bishop.color:
                    if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)):
                        self.addMove(bishop, takePos)
                        break
                else:
                    break
            else:
                if ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)): 
                    self.addMove(bishop, takePos)
 
    # loadqmoves
    # loads queen moves for all queens
    def loadqmoves(self, queen):
        # queen moves is a combination of rook and bishop moves:
        self.loadrmoves(queen)
        self.loadbmoves(queen)

    # loadkmoves
    # loads king moves for all kings
    def loadkmoves(self, king):
        pos = king.position
        #check squares around king
        for takePos in [pos + 8, pos - 8, pos + 9, pos - 9, pos + 1, pos - 1, pos + 7, pos -7]:
            # check if takePos is in the right constraints
            # check if takePos file is different by pos rank by only 1
            if ((0 <= takePos <= 63) and (abs(pos % 8 - takePos % 8) <= 1)):
                if takePos not in self.pieceList or self.pieceList[takePos].color != king.color:
                    # check if the square that the king wants to go to is already being attacked
                    if ((king.color == "w" and takePos not in self.blackLegalMoves) or (king.color == "b" and takePos not in self.whiteLegalMoves)):
                        self.addMove(king, takePos)

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

        # delete en passant'ed pawn if needed
        # need to check if the enpassant is ACTUALLY done
        if (piece.type == "p" and 
            self.enpassantPawnPos != -1 and
            (dest - self.enpassantPawnPos) == 8 * col
            ):
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

        # check if its a king to track the position of it
        if (piece.type == "k"):
            self.kings[piece.color] = piece.position

        # # check how many moves since last pawn move
        # if piece.type != 'p':
        #     self.MovesSinceLastPawn += 1 if self.turn == 'b' else 0
        # else:
        #     self.MovesSinceLastPawn = 0
        # self.checkDict = defaultdict(lambda: [])
        # self.whiteLegalMoves.clear()
        # self.blackLegalMoves.clear()
        # self.lineOfCheck = set()


        # after you move, clear the movedict, and checkdict
        self.moveDict.clear()
        print("movedict has been cleared")
        self.checkDict.clear()
        print("checkdict has been cleared")
        self.whiteLegalMoves.clear()
        self.blackLegalMoves.clear()
                    
        self.generateMoves(self.turn)
        self.turn = 'w' if self.turn == 'b' else 'b'
        # generate new moves after making a move
        self.lineOfCheck.clear()
        self.isInCheck(self.turn)
        self.moveDict.clear()
        self.generateMoves(self.turn)


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
            # switch colors
            # add reverted moves to unmadeMoves:
            self.unmadeMoves.append((previousOrigin, previousDest))

            self.generateMoves(self.turn)
            self.turn = 'w' if self.turn == 'b' else 'b'
            # generate new moves after making a move
            self.isInCheck(self.turn)
            self.generateMoves(self.turn)

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