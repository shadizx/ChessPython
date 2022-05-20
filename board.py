# board.py
# responsible for boad structure and operations
import pygame
from copy import copy
import piece
from dataclasses import dataclass
from collections import defaultdict

###################### constants ############################
WIDTH, HEIGHT = 1000, 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
FPS = 60                                       # setting fps of game
DIMENSION = HEIGHT//8                           # dimension of each square
DEFAULTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
#TIMES FOR GAMES
BLITZ = 180
BULLET = 60
RAPID = 600
CLASSICAL = 1800 
fileletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
###################################################################
# sounds for moving pieces
# pygame.mixer.init()
# moveSound = pygame.mixer.Sound("sounds/move.ogg")
# takeSound = pygame.mixer.Sound("sounds/capture.ogg")
# mateSound = pygame.mixer.Sound("sounds/mate.ogg")
# drawSound = pygame.mixer.Sound("sounds/draw.ogg")
# loseSound = pygame.mixer.Sound("sounds/defeat.ogg")
# startSound = pygame.mixer.Sound("sounds/welcome.ogg")
###################################################################

################################BOARD ANIMATIONS###################################
# shadeboard()
def shadeBoard():
    s = pygame.Surface((HEIGHT,HEIGHT))     # the size of your rect
    s.set_alpha(160)                        # translucency level
    s.fill((0, 0, 0, 127))                  # color of square
    win.blit(s, (0,0))                      # (0,0) are the top-left coordinates
###################################################################
# getmpos
# getting the position of the mouse upon clicking
def getmpos():
    pos = pygame.mouse.get_pos()
    x = pos[0] // 80
    y = 7 - pos[1] // 80
    return (x,y)
################################BOARD ANIMATIONS###################################

###################################################################
# class Board
# inherits from fen, responsible for board square colors
class Board:
    # start with this FEN
    FEN = DEFAULTFEN
    # FEN = DEFAULTFEN

    # holds boardcolors ( the squares )
    boardColors = []

    # dict that maps a piece to the legal moves of that piece
    # format: {p:[16,24]} - means a piece on square 8 can move to square 16 and 24
    moveDict = defaultdict(lambda: [])

    # list of moves that has happened so far:
    # used for going back a move, format is [(12, 20)] - means piece went from square 12 to square 20
    moveList = []
    annotationsList = []
    # tracks unmade moves to then go forward with arrow key
    unmadeMoves = []

    # tracks lost pieces to use in revertmove
    # maps the move number to a piece that was lost on that move
    # format" {5, q} means on move 5 a queen was "lost" or disappeared from the board
    lostPieces = {}

    # tracks number of moves that have been played
    moveCounter = 0
    
    # to check if enpassant is available
    enpassantPawnPos = -1

    # dictionary that maps a position that a piece(s) can go to, to the pieces that can go there
    # format: {43, [p,k,r]}
    # this means that the pawn king and rook can all go to square 43
    checkDict = defaultdict(lambda: [])

    # dict that tracks the kings position
    # format: {"w" : 4, "b" : 60} means white king is on square 4 and black is on 60
    kings = {}

    # line of check set
    # set that contains the line of check (positions)
    # format: (0,1,2,3) means that the side in check must cover one of these squares to block the check
    lineOfCheck = set()

    # pinnedPieces dict
    # contains the pinned pieces. key is the pinnned piece pos, and value is the pinning piece pos
    # format: {11: 32} means a piece on square 11 is pinned by a piece on square 32
    pinnedPieces = defaultdict(lambda: [])


    # line of pin set 
    # contains the positions that is in the line of pin
    lineOfPin = set()

    # incheck boolean set to check if king is in check
    inCheck = False

    # two dicts for where each piece can reach (including its own pieces)
    whiteReach = defaultdict(lambda: [])
    blackReach = defaultdict(lambda: [])

    # two sets for strictly the entire white and black moves
    whiteLegalMoves = set()
    blackLegalMoves = set()

    # two integers, each for the total white and black points 
    totalWhitePoints = 0
    totalBlackPoints = 0

    # whitePoints = totalWhitePoints - totalBlackPoints ----> How many points white is up
    # blackPoints = totalBlackPoints - totalWhitePoints ----> How many points black is up
    whitePoints = 0
    blackPoints = 0

    # see if board is in promotion state
    promotionState = False

    # maps move number to the piece that was promoted on that move
    promotedPieces = {}

    # save the pawns that promoted
    promotedPawns = {}

    def __init__(self):
        self.pieceList, self.turn, self.castlingsAllowed, self.enpassantSquare, self.movesSinceLastPawn, self.moveNumber, self.kings = fen(self.FEN).LoadFromFEN()
        if self.turn == "w":
            self.generateMoves("b")
            self.generateMoves("w")
        else:
            self.generateMoves("w")
            self.generateMoves("b")

    # generateMoves
    # useful for generating the moves of board
    def generateMoves(self, turn):
        # check if there are only two kings remaining so it would be a draw
        if len(self.pieceList) == 2 and self.kings["w"] in self.pieceList and self.kings["b"] in self.pieceList:
            print("Draw")
            return 0
        
        # clear the moveDict
        for piece in self.pieceList.values():
            if piece.color == turn:
                # check if a double check has happened, only the king can move then
                if self.kings[turn] in self.checkDict:
                    if len(self.checkDict[self.kings[turn]]) > 1:
                        print("double check")
                        self.loadkmoves(self.pieceList[self.kings[turn]])
                        break
                # add the Black pieces' points to the totalBlackPoints
                if turn == 'b':
                    self.totalBlackPoints += piece.value
                # add the White pieces' points to the totalWhitePoints
                else: 
                    self.totalWhitePoints += piece.value

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
        
        # Determining how many points the white is up from the black
        if self.totalWhitePoints > self.totalBlackPoints:
            self.whitePoints = self.totalWhitePoints - self.totalBlackPoints
            self.blackPoints = 0
        # Determining how many points the black is up from the white
        elif self.totalWhitePoints < self.totalBlackPoints:
            self.blackPoints = self.totalBlackPoints - self.totalWhitePoints
            self.whitePoints = 0
        # making both blackPoints and whitePoints if they have the same points in total
        else:
            self.blackPoints, self.whitePoints = 0, 0
    
        # now see if a side is in checkmate
        # this happens when you're in check and have no legal moves to make
        if (turn == "w" and len(self.whiteLegalMoves) == 0) or (turn == "b" and len(self.blackLegalMoves) == 0):
            if self.kings[turn] in self.checkDict:
                print("Checkmate!")
                return 2
            else:
                print("Stalemate!")
                return 1

    # addmove
    # adds a legal move to the appropriate dictionaries
    def addMove(self, piece, dest):
        self.moveDict[piece].append(dest)
        if dest in self.pieceList:
            self.checkDict[dest].append(piece)
        if piece.color == "w":
            self.whiteReach[dest].append(piece)
            self.whiteLegalMoves.add(dest)
        else:
            self.blackReach[dest].append(piece)
            self.blackLegalMoves.add(dest) 

    # function for checking if king is in check in O(1) time
    # updates the line of check set efficiently 
    def isInCheck(self, color):
        # check if position of the king is in the legal moves
        # if it is, it updates the line of check

        # get kings position
        kingPos = self.kings[color]
        kingRank, kingFile = piece.getRankFile(kingPos)
        # if the king is in check

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
            # check if takepos's file is only 1 different with current file
            if abs(takePos % 8 - pos % 8) == 1:
                # if you're in check and can take the piece, or you are not in check
                checkRestriction = (self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)
                # if you're not pinned, or you're pinned but you can take the pinned piece
                pinRestriction = (pos not in self.pinnedPieces) or (self.pinnedPieces[pos] == takePos)

                # for each square that we are checking, there is either a piece on that square or not.
                # first lets check if there is a piece there:
                if takePos in self.pieceList:
                    # now there are two cases, either there is a same color piece here, or opponent
                    # if there is a same color piece here, make sure this piece is protecting that
                    if self.pieceList[takePos].color == pawn.color:
                        self.whiteReach[takePos].append(pawn) if pawn.color == "w" else self.blackReach[takePos].append(pawn)
                    # if there is a different colored piece on this square, see if we can take it:
                    # you must be not pinned, and pass check restriction
                    elif pinRestriction and checkRestriction:
                        self.addMove(pawn, takePos)
                # if there is no piece on a square, see if we can move there
                else:
                    # if there is no piece on this square, you cannot take diagonally
                    # if you are pinned or you are in check, you still need to defend these squares
                    self.whiteReach[takePos].append(pawn) if pawn.color == "w" else self.blackReach[takePos].append(pawn)       
        #######################################################################
        # calculating en passant moves:
        # parameters for an en passant move is:
        #   1) if previous move was a pawn move played to the exact right or left of a pawn
        #   2) and this happens on rank 5 (for white) and rank 4 (for black)

        # check if there has been a move played
        if len(self.moveList) != 0:
            # get coordinates of the other peice's position (last position and current one)
            otherPiecePos = (self.moveList[-1])[1]
            # [(8,24),(62,54)]
            otherPiecePrevPos = (self.moveList)[-1][0]
            # get rank and file from otherPiecePos
            otherPieceRank, otherPieceFile = piece.getRankFile(otherPiecePos)
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
                    # if your pawn is not pinned, or its pinned and can take and still be pinned
                    (pos not in self.pinnedPieces or (pos in self.pinnedPieces and otherPiecePos + 8 * col in self.lineOfPin)) and
                    # you're not in check, or you're in check and you can take the checking piece
                    ((self.inCheck and (otherPiecePos in self.lineOfCheck)) or (not self.inCheck))
            ):
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
                # if you're in check and can take the piece, or you are not in check
                checkRestriction = (self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck)
                # for each square that we are checking, there is either a piece on that square or not.
                # first lets check if there is a piece there:
                if takePos in self.pieceList:
                    # now there are two cases, either there is a same color piece here, or opponent
                    # if there is a same color piece here, make sure this piece is protecting that
                    if self.pieceList[takePos].color == knight.color:
                        self.whiteReach[takePos].append(knight) if knight.color == "w" else self.blackReach[takePos].append(knight)
                    # if there is a different colored piece on this square, see if we can take it:
                    # you must be not pinned, and pass check restriction
                    elif pos not in self.pinnedPieces and checkRestriction:
                        self.addMove(knight, takePos)
                # if there is no piece on a square, see if we can move there
                else:
                    # if you are not pinned and not in check you can move to this empty square
                    if pos not in self.pinnedPieces and checkRestriction:
                        self.addMove(knight, takePos)
                    # if you are pinned or you are in check, you still need to defend these squares
                    else:
                        self.whiteReach[takePos].append(knight) if knight.color == "w" else self.blackReach[takePos].append(knight)

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
            firstAdd = True
            # used for seeing if the pinned piece can move, later added to line of pin
            pinLine = set()
            for takePos in range(startList[i], endList[i], incList[i]):
                # if you're in check and can take the piece, or you are not in check
                checkRestriction = ((self.inCheck and (takePos in self.lineOfCheck)) or (not self.inCheck))
                # if you're not pinned, or you're pinned but you can take the pinned piece
                pinRestriction = (pos not in self.pinnedPieces) or (self.pinnedPieces[pos] == takePos) or (pos in self.pinnedPieces and takePos in self.lineOfPin)

                # for each square that we are checking, there is either a piece on that square or not.
                # first lets check if there is a peice there:
                if takePos in self.pieceList:
                    # now there are two cases, either there is a same color piece here, or opponent
                    # if there is a same color piece here, make sure this piece is protecting that, then break because rest squares in that dir don't matter
                    if self.pieceList[takePos].color == p.color:
                        self.whiteReach[takePos].append(p) if p.color == "w" else self.blackReach[takePos].append(p)
                        break
                    # now check if there is an opponent piece on this square
                    # if this is the first opp piece, and we are not in check or pinned, then add this to our movedict
                    if firstAdd and checkRestriction and pinRestriction:
                        self.addMove(p, takePos)
                        # save this position, incase it is a pinned piece
                        posInBetween = takePos
                        firstAdd = False
                    # now if it is not the first time adding an opponent piece, it must either be a king, or we will break
                    elif not firstAdd:
                        # if it is a king, and the posinbetween location to our pinned pieces list and break
                        if self.pieceList[takePos].type == "k":
                            self.pinnedPieces[posInBetween] = pos
                            self.lineOfPin = pinLine | self.lineOfPin
                        # if it is not a king on our second add, then break because there is no point
                        break
                # now check if this position is an empty square
                # if its the first time you are adding
                elif firstAdd:
                    pinLine.add(takePos)
                    # if we are adding an empty square on the first time, our piece can move there if we are not in check or not pinned
                    if pinRestriction and checkRestriction:
                        self.addMove(p, takePos)
                    else:
                        self.whiteReach[takePos].append(p) if p.color == "w" else self.blackReach[takePos].append(p)
                # if it's not your second add, and you are looking at an empty square, do nothing and keep going
                # KEEP GOING UNLESS THE FIRSTADDED PIECE WAS A KING, TO GET SQUARES BEHIND KING
                elif not firstAdd:
                    pinLine.add(takePos)
                    oppcol = "b" if p.color == "w" else "w"
                    if posInBetween == self.kings[oppcol]:
                        self.whiteReach[takePos].append(p) if p.color == "w" else self.blackReach[takePos].append(p)
                        break
        # now check if the piece is pinned and can still move in the line of pin

    # loadkmoves
    # loads king moves for all kings
    def loadkmoves(self, king):
        pos = king.position
        #check squares around king
        # print("##################################################################################################")
        # print("my turn is ", king.color, "my pos is ", pos, "whitelegalmoves is ", str(self.whiteLegalMoves), "blacklegalmoves is ", str(self.blackLegalMoves))
        # print("\n\n")
        for takePos in [pos + 8, pos - 8, pos + 9, pos - 9, pos + 1, pos - 1, pos + 7, pos -7]:
            # check if takePos is in the right constraints
            # check if takePos file is different by pos rank by only 1
            if ((0 <= takePos <= 63) and (abs(pos % 8 - takePos % 8) <= 1)):
                if takePos not in self.pieceList or self.pieceList[takePos].color != king.color:
                    # check if the square that the king wants to go to is already being attacked
                    if ((king.color == "w" and takePos not in self.blackReach) or (king.color == "b" and takePos not in self.whiteReach)):
                        self.addMove(king, takePos)
                elif self.pieceList[takePos].color == king.color:
                        self.whiteReach[takePos].append(king) if king.color == "w" else self.blackReach[takePos].append(king)
        # now lets check for castles
        # calculate short castle first
        # restrictions for castling are:
        #   1) king and rook has not moved
        #   2) the line of squares of castling should be empty and not attackable
        if king.hasMoved == False:
            # check short castle
            # sqaures of short castles are:
            shortCastleSquares = set({pos + 1, pos + 2})
            longCastleSquares  = set({pos - 1, pos - 2, pos - 3})
            longKingRoute = set({pos - 1, pos - 2})

            shortRookPos, longRookPos = -1,-1
            if pos + 3 in self.pieceList:
                shortCastleRook = self.pieceList[pos + 3]
                shortRookPos = pos + 3
            if pos - 4 in self.pieceList:
                longCastleRook = self.pieceList[pos - 4]
                longRookPos = pos - 4

            # check for shortcastle
            if (
                # if there are no pieces in the range of shortcastlesquares:
                len(shortCastleSquares.intersection(self.pieceList)) == 0 and
                # check if rook is where its supposed to be with the right color and it hasn't moved
                shortRookPos in self.pieceList and shortCastleRook.type == "r" and shortCastleRook.color == king.color and shortCastleRook.hasMoved == False and
                # your king cannot be in check
                (self.kings[king.color] not in self.checkDict) and
                # the squares in between castle can't be attackable
                (len(shortCastleSquares.intersection(self.whiteLegalMoves)) == 0 if king.color == "b" else len(shortCastleSquares.intersection(self.blackLegalMoves)) == 0)
            ):
                self.addMove(king, pos + 2)
            
            # check for long castle
            if (
                # if there are no pieces in the range of longcastlesquares
                len(longCastleSquares.intersection(self.pieceList)) == 0 and
                # check if rook is where its supposed to be with the right color and it hasn't moved
                longRookPos in self.pieceList and longCastleRook.type == "r" and longCastleRook.color == king.color and longCastleRook.hasMoved == False and
                # your king cannot be in check
                (self.kings[king.color] not in self.checkDict) and
                # the squares in between castle can't be attackable
                (len(longKingRoute.intersection(self.whiteReach)) == 0 if king.color == "b" else len(longKingRoute.intersection(self.blackReach)) == 0)
            ):
                self.addMove(king, pos - 2)

    # promotePiece
    # does the animation and functions for promoting a piece
    def promotePiece(self, p, origin, dest, autoComplete = None):

        # if autocomplete is true, then just return the autocompleted piece
        if autoComplete is not None:
            # add piece to piecelist
            self.pieceList[origin] = autoComplete
            self.pieceList[origin].setPos(dest)
            # change p to point to this piece
            p = self.pieceList[origin]
            # change origin to the origin of this new piece
            return p

        # for the promotion animation, we need to shade the board, and draw four opaque circles and on each circle draw a knight queen rook and bishop
        # 1) shade the board:
        circleColor = (128,128,128)
        col = p.color
        colNum = -1 if col == "w" else 1
        pos = dest
        rank,file = piece.getRankFile(dest)
        shadeBoard()

        # get the images of the pieces to print
        pieceList = [piece.queen(col, pos), piece.knight(col, pos + 8 * colNum), piece.rook(col, pos + 16 * colNum), piece.bishop(col, pos + 24 * colNum)]
        pieceDict = {pos : piece.queen(col, pos), pos + 8 * colNum: piece.knight(col, pos + 8 * colNum), pos + 16 * colNum: piece.rook(col, pos + 16 * colNum), pos + 24 * colNum: piece.bishop(col, pos + 24 * colNum)}

        for i in range(4):
            offsetx = 2 * (8 - file) - 1
            circlex = HEIGHT - (DIMENSION/2 * offsetx)
            offsety = 2 * (8 - rank) - 1
            circley = DIMENSION/2 * offsety
            # change rank
            if col == "w":
                rank -= 1
            else:
                rank += 1
            # draw each circle
            pygame.draw.circle(win, circleColor, (circlex, circley), DIMENSION/2)
            #draw each piece
            pieceList[i].draw()
        # update window
        pygame.display.update()
        self.promotionState = True

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # if program is executed
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: # if left-clicked
                        xpos = getmpos()[0]
                        ypos = getmpos()[1]
                        mousepos = 8 * ypos + xpos
                        # if clicked on one of the pieces
                        if mousepos in pieceDict:
                            # add piece to piecelist
                            self.pieceList[origin] = pieceDict[mousepos]
                            self.pieceList[origin].setPos(pos)
                            # change p to point to this piece
                            p = self.pieceList[origin]
                            # change origin to the origin of this new piece
                            return p
                        else:
                            return -1

    # makeMove
    # useful for moving a piece and updating our directory accordingly
    def makeMove(self, origin, dest, forced = None):
        # annotation arguments
        piece_type = '' 
        take_indicator = False
        promotion_target = ''
        castle_overwrite = 0


        self.moveCounter += 1
        print("on move", self.moveCounter)

        self.promotionState = False
        autoComplete = None

        # grab the piece, move it to the destination
        p = self.pieceList[origin]
        piece_type=p.type
        # get color of piece
        col = 1 if p.color == "w" else -1

        ###################### AUTOCOMPLETE #########################
        # check if the move made is not the same as the last unmade move
        # this means that we should pop the last unmade move because we are on a different branch
        if len(self.unmadeMoves) > 0:
            differentLastMove = (origin, dest) != self.unmadeMoves.pop()
            if (differentLastMove and self.moveCounter not in self.promotedPieces):
                self.unmadeMoves.clear()
            elif self.moveCounter in self.promotedPieces and not differentLastMove:
                # if movecounter is in self.promotedpieces then this means we have played this promotion before
                # and we want to auto complete it
                if forced is not None:
                    autoComplete = self.promotedPieces.pop(self.moveCounter)
                
        ################# PIECE BEING TAKEN #######################
        # if there is a piece being taken track that
        if dest in self.pieceList:
            self.lostPieces[self.moveCounter] = self.pieceList[dest]
            take_indicator = True
            # pygame.mixer.Sound.play(takeSound)
            print("TAKEN PIECE ON MOVE", self.moveCounter)
        # else:
        #     pygame.mixer.Sound.play(moveSound)

        ###################### ENPASSANT ###########################
        # delete en passant'ed pawn if needed
        # need to check if the enpassant is ACTUALLY done
        if (p.type == "p" and 
            self.enpassantPawnPos != -1 and
            (dest - self.enpassantPawnPos) == 8 * col
            ):
            # add to lost pieces so we can bring back the piece
            self.lostPieces[self.moveCounter] = self.pieceList[self.enpassantPawnPos]
            del self.pieceList[self.enpassantPawnPos]
            self.enpassantPawnPos = -1
            take_indicator = True
            print("EN CHOSSANT HAS BEEN TAKEN")

        ###################### PROMOTION ###########################
        # check if piece is promoting:
        # if on the last rank for white or on the first rank for black
        if (dest // 8 == 7 and p.color == "w" and p.type == "p") or (dest // 8 == 0 and p.color == "b" and p.type == "p"):
            print("promoting")
            promotedPiece = self.promotePiece(p, origin, dest, autoComplete)
            if promotedPiece == -1:
                return
            # add to lost pieces for reverting moves
            self.promotedPawns[self.moveCounter] = p
            p = copy(promotedPiece)
            promotion_target = p.type
            # add to promotedpieces to track if we go forward
            self.promotedPieces[self.moveCounter] = p
        

        ###################### MOVING PIECE ###########################
        # move the piece to its destination
        p.setPos(dest)
        # update the position of the piece in pieceList
        self.pieceList[dest] = self.pieceList.pop(origin)  # YES, this also deletes the piece in origin
        # add the move to moveList
        self.moveList.append((origin, dest))

        # check if its a rook or king to update that they have been moved and no longer to castle:
        if (p.type in ("k", "r")):
            # if it's the first time the king/rook moves track that
            if p.hasMoved == False:
                p.firstMove = self.moveCounter
            p.hasMoved = True

        ##################### CASTLING AND KINGS #######################
        # check if its a king to track the position of it
        if (p.type == "k"):
            self.kings[p.color] = p.position
            # check if the king wants to castle to move the rook as well
            if dest - origin == 2:
                # this means that the king wants to short castle
                # get position of rook
                rook = self.pieceList[origin + 3]
                # move the piece to its destination
                rook.setPos(origin + 1)
                # update the position of the piece in pieceList
                self.pieceList[origin + 1] = self.pieceList.pop(origin + 3)
                # update hasmoved of rook
                rook.hasMoved = True
                castle_overwrite = 1

            elif dest - origin == -2:
                # this means that the king wants to long castle
                # get position of rook
                rook = self.pieceList[origin - 4]
                # move the piece to its destination
                rook.setPos(origin - 1)
                # update the position of the piece in pieceList
                self.pieceList[origin - 1] = self.pieceList.pop(origin - 4)
                # update hasmoved of rook
                rook.hasMoved = True
                castle_overwrite = 2

        ####################### 50 MOVE RULE ############################
        # check how many moves since last pawn move
        if p.type != 'p':
            self.movesSinceLastPawn += 1 if self.turn == 'b' else 0
        else:
            self.movesSinceLastPawn = 0

        ########################  ANNOTATE   ############################
        annotation = self.annotateMove(origin, dest, piece_type, take_indicator, promotion_target, castle_overwrite)
        ######################## DIRECTORIES ############################

        self.checkDict.clear()
        self.whiteReach.clear()
        self.blackReach.clear()
        self.pinnedPieces.clear()
        self.lineOfPin.clear()
        self.moveDict.clear()
        self.whiteLegalMoves.clear()
        self.blackLegalMoves.clear()
        # setting both the totalWhitePoints and the totalBlackPoints to zero so that they don't double every time we make a move.
        self.totalWhitePoints = 0
        self.totalBlackPoints = 0

        self.lineOfCheck.clear()
        # self.isInCheck(self.turn)
        # generate new moves for the same side after they turned, to see if the other side is in check
        if res:=self.generateMoves(self.turn) in [0,1,2]:
            if res == 1:
                annotation+=('#')
                self.annotationsList.append(annotation)
            return
        # switch the move
        self.turn = 'w' if self.turn == 'b' else 'b'

        # clear line of check and see if other side is in check
        self.lineOfCheck.clear()
        self.isInCheck(self.turn)
        self.moveDict.clear()
        # generate moves for other side
        if res:=self.generateMoves(self.turn) in [0,1,2]:
            if res == 1:
                annotation+=('#')
                self.annotationsList.append(annotation)
            return
        if self.inCheck:
            annotation+=('+')
        self.annotationsList.append(annotation)
        

    def revertMove(self):
        if self.moveCounter != 0:
            # grab origin and dest of last move played
            previousOrigin, previousDest = (self.moveList.pop(-1))  # removes and returns the last element
            self.annotationsList.pop()
            # grab the piece
            p = self.pieceList.pop(previousDest)
            pos = p.position

            # check if a castle was made to revert the castle
            if p.type == "k":
                # if short castle:
                if previousDest - previousOrigin == 2:
                    # move pieces back to original spots
                    # get position of rook
                    rook = self.pieceList[pos - 1]
                    # move the piece to its original position
                    rook.setPos(previousOrigin + 3)
                    # update the position of the piece in pieceList
                    self.pieceList[previousOrigin + 3] = self.pieceList.pop(pos - 1)
                    # update hasmoved of rook
                    rook.hasMoved = False
                    p.hasMoved = False
                # long castle:
                elif previousDest - previousOrigin == -2:
                    # get position of rook
                    rook = self.pieceList[pos + 1]
                    # move the piece to its original position
                    rook.setPos(previousOrigin - 4)
                    # update the position of the piece in pieceList
                    self.pieceList[previousOrigin - 4] = self.pieceList.pop(pos + 1)
                    # update hasmoved of rook
                    rook.hasMoved = False
                    p.hasMoved = False

            # check if a king/rook returned to its original position so we'll turn hasMoved to false
            if p.type in ["k","r"]:
                # check if the king returned back to its first position
                if p.firstMove == self.moveCounter:
                    p.hasMoved = False
                    p.firstMove = -1

            p.setPos(previousOrigin)
            self.pieceList[previousOrigin] = p

            # see if there was a piece taken on previous dest
            # bring it back to life
            if (self.moveCounter in self.lostPieces):
                lostPiece = self.lostPieces.pop(self.moveCounter)
                self.pieceList[lostPiece.position] = lostPiece
            
            # check if reverting a promotion move, need to bring back the pawn
            if (self.moveCounter in self.promotedPawns):
                lostPawn = self.promotedPawns.pop(self.moveCounter)
                self.pieceList[lostPawn.position] = lostPawn
            
            self.moveCounter -= 1
            # add reverted moves to unmadeMoves:
            self.unmadeMoves.append((previousOrigin, previousDest))

            self.checkDict.clear()
            self.whiteReach.clear()
            self.blackReach.clear()
            self.pinnedPieces.clear()
            self.lineOfPin.clear()
            self.moveDict.clear()
            self.whiteLegalMoves.clear()
            self.blackLegalMoves.clear()

            self.lineOfCheck.clear()
            # self.isInCheck(self.turn)
            # generate new moves for the same side after they turned, to see if the other side is in check
            if self.generateMoves(self.turn) in [0,1,2]:
                return
            # switch the move
            self.turn = 'w' if self.turn == 'b' else 'b'

            # clear line of check and see if other side is in check
            self.lineOfCheck.clear()
            self.isInCheck(self.turn)
            
            self.moveDict.clear()
            # generate moves for other side
            if self.generateMoves(self.turn) in [0,1,2]:
                return
    # annotate the move
    # takes place after the table has been updated but before the Reach dictionary has been cleared
    # does not work for check; the code will add that later manually.
    def annotateMove(self, origin:int, dest:int, piece_type:str, take_indicator:bool, promotion_target:str, castle_overwrite:int):
        '''
        Annotates the move in standard chess notation.
        Does not work for check; the code will add that later manually.
        '''
        # castles are a special case, so handled differently
        if castle_overwrite == 1: # short castle
            return "O-O"
        if castle_overwrite == 2: # long castle
            return "O-O-O"
        
        annotation = ""
        # indicate origin
        # pawns are annotated slightly differently, so their case is separated.
        if piece_type != "p":
            annotation+=(piece_type.upper())
            # now check for duplicates in destination
            reach = self.whiteReach if self.turn == "w" else self.blackReach
            samefile = samerank = morethanone = False
            for piece in reach[dest]:
                if piece.type == piece_type and piece.position != dest:
                    if piece.position%8 == origin%8:
                        samefile = True
                    elif piece.position//8 == origin//8:
                        samerank = True
                    morethanone = True
            if samerank:
                annotation+=(fileletters[origin%8]) # name the file
            if samefile:
                annotation+=(str(origin//8+1)) # name the rank
            if (not samerank) and (not samefile) and morethanone:
                annotation+=(fileletters[origin%8]) # standard
        else:
            annotation+=(fileletters[origin%8]) # only name the file for pawns
        # indicate take
        if take_indicator:
            annotation+=('x')
        # indicate destination of piece
        if piece_type != 'p' or take_indicator:
            annotation+=(f"{fileletters[dest%8]}{dest//8+1}")
        else:
            annotation+=(str(dest//8+1))
        # indicate if promotion has happened (only for pawns, obviously!)
        if promotion_target != '':
            annotation+=(f"={promotion_target.upper()}")
        return annotation

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

                if piece.type == "k" and piece.color == "w":
                    self.wKing = piece.position
                elif piece.type == "k" and piece.color == "b":
                    self.bKing = piece.position

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

        return (self.pieces, self.Turn, self.CastlingsAllowed, self.EnPassantSquare, self.MovesSinceLastPawn, self.MoveNumber, {"w": self.wKing, "b" : self.bKing})

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
        pygame.draw.rect(win, self.color, pygame.Rect(x * DIMENSION, HEIGHT - (y+1) * DIMENSION, DIMENSION, DIMENSION))

# class square
###################################################################
# class Move:
#     origin, destination = (0, 0)
#     piece_type = None
#     taken_piece = None
#     check_indicator = None
#     promotion_target = None
#     castle_rook_tracker = None
#     hasmoved_change = None
#     def __repr__(self) -> str:
#         pass
