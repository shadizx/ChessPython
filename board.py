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
DEFAULTFEN = "//3k3pn//3QB/// w KQkq - 0 1"
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
    # pinnedPieces dict
    # contains the pinned pieces. key is the pinnned piece pos, and value is the pinning piece pos 
    pinnedPieces = defaultdict(lambda: [])
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
                elif piece.type == "n":
                    self.loadnmoves(piece)
                elif piece.type in ("r", "b"):
                    self.loadSlidingMoves(piece)
                elif piece.type == "q":
                    self.loadSlidingMoves(piece, 0)
                    self.loadSlidingMoves(piece, 1)
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
                if oppPiece.type in ("r","q"):
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
        # if the position in front of the pawn is empty and you're not pinned
        pawnUpInPin = (pos in self.pinnedPieces) and (self.kings[pawn.color] % 8 == pos % 8)
        if pos + 8 * col not in self.pieceList and (pos not in self.pinnedPieces or pawnUpInPin):
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
            canMove = (abs((takePos % 8) - (pos % 8)) == 1) and ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck))
            if canMove:
                # if you're pinned and you cannot attack the piece, then you have no moves with this pawn
                if takePos in self.pieceList:
                    if (pos not in self.pinnedPieces and self.pieceList[takePos].color != pawn.color) or (self.pinnedPieces[pos] == takePos):
                        self.addMove(pawn, takePos)
                    else:
                        self.whiteLegalMoves[takePos].append(pawn) if pawn.color == "w" else self.blackLegalMoves[takePos].append(pawn)
                else:
                    self.whiteLegalMoves[takePos].append(pawn) if pawn.color == "w" else self.blackLegalMoves[takePos].append(pawn)
        #######################################################################
        # calculating en passant moves:
        # parameters for an en passant move is:
        #   1) if previous move was a pawn move played to the exact right or left of a pawn
        #   2) and this happens on rank 5 (for white) and rank 4 (for black)

        # check if there has been a move played
        if len(self.moveList) != 0 and pos not in self.pinnedPieces:
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
                canMove = (self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)
                if canMove:
                    if (takePos in self.pieceList):
                        if (pos not in self.pinnedPieces and self.pieceList[takePos].color != knight.color):
                                self.addMove(knight, takePos)
                        elif self.pieceList[takePos].color == knight.color:
                                self.whiteLegalMoves[takePos].append(knight) if knight.color == "w" else self.blackLegalMoves[takePos].append(knight)
                    else:
                        if pos not in self.pinnedPieces:
                            self.addMove(knight, takePos)

    # loadSlidingMoves
    # loads moves for queen bishop and rook
    def loadSlidingMoves(self, p, queenOption = None):
        pos = p.position
        rank,file = piece.getRankFile(pos)
        # start and end index differs based on piece type
        if p.type == "r" or queenOption == 0:
            startList = [pos + 8, pos - 8, pos + 1, pos - 1]
            endList =   [64, file - 1, 8 * (rank + 1), 8 * rank - 1]
            incList =   [8,-8,1,-1]
        elif p.type == "b" or queenOption == 1:
            limNE = (7 - max(rank, file)) * 9 + pos
            limNW = min(file, 7 - rank) * 7 + pos
            limSE = pos - min(7 - file, rank) * 7
            limSW = pos - min(rank, file) * 9

            startList = [pos + 9, pos + 7, pos - 7, pos - 9]
            endList =   [limNE + 1, limNW + 1, limSE - 1, limSW - 1]
            incList =   [9,7,-7,-9]

        for i in range(4):
            posInBetween = -1
            pieceInBetween = set()
            firstAdd = True
            for takePos in range(startList[i], endList[i], incList[i]):
                checkRestriction = ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck))
                # if you're not pinned, or you're pinned but you can take the pinned piece
                pinRestriction = pos not in self.pinnedPieces or (self.pinnedPieces[pos] == takePos)
                # check if there is a piece on a square
                # also check if you are even able to move ther (with checkrestriction)
                if checkRestriction:
                    if takePos in self.pieceList:
                        # if same color piece on that square, and that to the legal moves of that piece and break
                        # we do this so the piece is "protecting" the other piece, so king cant take
                        if self.pieceList[takePos].color == p.color:
                            self.whiteLegalMoves[takePos].append(p) if p.color == "w" else self.blackLegalMoves[takePos].append(p)
                            break
                        else:
                        # now we are checking if there is a piece on this square that is the opposite color of our piece
                        # if this is the first enemy piece we encounter, add this to our legal moves (and only this)
                        # we also add this enemy piece to the pinnedPieces, to see if its the only piece standing in the way of check
                            if firstAdd:
                                self.addMove(p, takePos)
                                posInBetween = takePos
                                firstAdd = False
                            # if our second piece is not a king, then there are no pinned pieces and break
                            elif self.pieceList[takePos].type != "k":
                                break
                            else:
                                # if it is a king, then there is a piece pinned!
                                self.pinnedPieces[posInBetween] = pos
                    else:
                        # if no piece on that square, append move and keep going
                        if firstAdd == True:
                            self.addMove(p,takePos)
                        else:
                            self.whiteLegalMoves[takePos].append(p) if p.color == "w" else self.blackLegalMoves[takePos].append(p)
                            break        

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

        # after you move, clear all the dicts
        self.moveDict.clear()
        self.checkDict.clear()
        self.whiteLegalMoves.clear()
        self.blackLegalMoves.clear()
        self.pinnedPieces.clear()
        # generate new moves for the same side after they turned, to see if the other side is in check
        self.generateMoves(self.turn)
        # switch the move
        self.turn = 'w' if self.turn == 'b' else 'b'
        # clear line of check and see if other side is in check
        self.lineOfCheck.clear()
        self.isInCheck(self.turn)
        self.moveDict.clear()
        # generate moves for other side
        self.generateMoves(self.turn)

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