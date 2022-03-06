# piece.py
# responsible for functionality of the pieces

import piecedirectory as pd
import pygame
import os
from copy import copy, deepcopy

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
filelist = ["a","b","c","d","e","f","g","h"]
ranklist = ["1","2","3","4","5","6","7","8"]
fileranks = {"a" : 0 ,"b" : 1 ,"c" : 2 ,"d" : 3 ,"e" : 4 ,"f" : 5 ,"g" : 6 ,"h" : 7}
DirectionOffsets = [(0,1), (1,0), (0,-1), (-1,0), (1,1), (1,-1), (-1,-1), (-1,1)]  # N E S W NE SE SW NW
KnightMoves = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2, 1), (-1, 2)]
###################### constants ########################### 
#   
def numtoletter(x, y):
    return (filelist[x] + ranklist[y])
#       
def tupletranslate(m):
    x = fileranks[m[0]]
    y = int(m[1]) - 1
    return((x,y))
#
def pieceinsquare(square):
    return pd.HYP_DIRECTORY[numtoletter(square[0], square[1])]

def findpiece(type, color):
    for s in pd.HYP_DIRECTORY:
        if pd.HYP_DIRECTORY[s] is not None:
            if (pd.HYP_DIRECTORY[s].type == type) and (pd.HYP_DIRECTORY[s].color == color):
                return tupletranslate(s)
############################################################   

# Class piece -------------------------------------------
# general parent class for each piece, is inherited from for efficient code
class Piece:
    # default constructor
    def __init__(self, color, type, file=0, rank=0, isPhantom = False):
        self.color = color
        self.selected = False  # if piece is selected
        self.hasmoved = False
        self.type = type
        self.img = pygame.image.load("assets/" + color + type + ".png")
        self.rect = self.img.get_rect()
        self.clicked = False
        self.moves = []
        self.file = file
        self.rank = rank
        self.isPhantom = isPhantom

    def setpos(self, file, rank):  # easy navigation
        self.file = file
        self.rank = rank
        if not self.isPhantom:
            pd.DIRECTORY[(filelist[file] + str(ranklist[rank]))] = self
            pd.HYP_DIRECTORY[(filelist[file] + str(ranklist[rank]))] = self

    # moving a piece to a destination
    def move(self, file, rank):
        pd.DIRECTORY[(filelist[self.file] + str(ranklist[self.rank]))] = None
        pd.HYP_DIRECTORY[(filelist[self.file] + str(ranklist[self.rank]))] = None
        self.file = file
        self.rank = rank
        pd.DIRECTORY[(filelist[file] + str(ranklist[rank]))] = self
        pd.HYP_DIRECTORY[(filelist[file] + str(ranklist[rank]))] = self
        pd.TURN = 'w' if pd.TURN == 'b' else 'b'
        pd.HYP_TURN = pd.TURN

    def move_hypothetical(self, file, rank):
        pd.HYP_DIRECTORY[(filelist[self.file] + str(ranklist[self.rank]))] = None
        self.file = file
        self.rank = rank
        pd.HYP_DIRECTORY[(filelist[file] + str(ranklist[rank]))] = self
        pd.HYP_TURN = 'w' if pd.HYP_TURN == 'b' else 'b'
    # checking if a piece is selected
    def isSelected(self):
        return self.selected

    # printing a piece on the board, centralized on their respective squares:
    def draw(self):
        offset = (dimension-piece_size)//2
        win.blit(self.img, ((dimension * self.file + offset - 3), (height - dimension * (self.rank + 1) + offset - 3)))
    
    def all_moves(self):  # only used for regular move generation
        phantom = Phantom(self.color, self.type, self.file, self.rank)
        moves = phantom.generate_moves()
        return moves

    def legalmoves(self):
        phantom = Phantom(self.color, self.type, self.file, self.rank)
        moves = phantom.generate_legal_moves()
        self.moves = moves
        return moves  # returns moves for easier access
# Class piece ---------------------------------------------
class Phantom(Piece):  # a piece without a type for measuring allowed movements
    def __init__(self, color, type,  file, rank):
        super().__init__(color, type=type, file=file, rank=rank, isPhantom=True)
        self.isSliding = self.type in ['b', 'r', 'q', 'k']
    
    def generate_slide (self):
        startDirIndex = 4 if self.type == 'b' else 0  # bishops can only do last 4 moves
        endDirIndex = 4 if self.type == 'r' else 8  # rooks can only do first 4 moves
        maxmoves = 2 if self.type == 'k' else 8  # kings can only move one square
        moveSquares = []
        for directionIndex in range(startDirIndex, endDirIndex):
            for n in range(1,maxmoves):  # moves up to 7 squares in a certain direction
                targetSquare = ((self.file)+n*DirectionOffsets[directionIndex][0], self.rank+n*DirectionOffsets[directionIndex][1])
                if (targetSquare[0] not in range (0,8)) or (targetSquare[1] not in range (0,8)):
                    break
                pieceOnTargetSquare = pieceinsquare(targetSquare)  # set to None if empty

                if pieceOnTargetSquare is not None:
                    if pieceOnTargetSquare.color == self.color:
                        break
                    else:
                        moveSquares.append(targetSquare)
                        break
                else:
                    moveSquares.append(targetSquare)  # talk about sloppy coding!
        return moveSquares
    
    def generate_pawn_move(self):
        moveSquares = []
        if self.color == "b":
            destination = (self.file, self.rank - 1)
            if pieceinsquare(destination) is None:
                moveSquares.append((destination))
            if (self.rank == 6):
                destination = (self.file, self.rank - 2)
                moveSquares.append(destination)
            if self.file > 0:  # only allow take on left on certain files
                destination = (self.file-1, self.rank-1)
                if pd.ENPASSANTSQUARE == destination:
                    moveSquares.append(destination)
                if pieceinsquare(destination) is not None:
                    if pieceinsquare(destination).color == 'w':
                        moveSquares.append(destination)
            if self.file < 7:  # allow take on right on certain files
                destination = (self.file+1, self.rank-1)
                if pd.ENPASSANTSQUARE == destination:
                    moveSquares.append(destination)
                if pieceinsquare(destination) is not None:
                    if pieceinsquare(destination).color == 'w':
                        moveSquares.append(destination)

        else:
            destination = (self.file, self.rank + 1)
            if pieceinsquare(destination) is None:
                moveSquares.append((destination))
            if (self.rank == 1):
                destination = (self.file, self.rank + 2)
                moveSquares.append(destination)
            if self.file > 0:  # only allow take on left on certain files
                destination = (self.file-1, self.rank+1)
                if pd.ENPASSANTSQUARE == destination:
                    moveSquares.append(destination)
                if pieceinsquare(destination) is not None:
                    if pieceinsquare(destination).color == 'b':
                        moveSquares.append(destination)
            if self.file < 7:  # allow take on right on certain files
                destination = (self.file+1, self.rank+1)
                if pd.ENPASSANTSQUARE == destination:
                    moveSquares.append(destination)
                if pieceinsquare(destination) is not None:
                    if pieceinsquare(destination).color == 'b':
                        moveSquares.append(destination)
        return moveSquares

    def generate_knight_move(self):
        moveSquares = []
        for x, y in KnightMoves:
            targetSquare = ((self.file)+x, self.rank+y)
            if (targetSquare[0] in range (0,8)) and (targetSquare[1] in range (0,8)):
                pieceOnTargetSquare = pieceinsquare(targetSquare)  # set to None if empty
                if pieceOnTargetSquare is not None:
                    if pieceOnTargetSquare.color != self.color:
                        moveSquares.append(targetSquare)
                else:
                    moveSquares.append(targetSquare)  # talk about sloppy coding!
        return moveSquares
    def generate_moves(self):
        moveSquares = []
        if pd.HYP_TURN == self.color:  # still obeys turns to avoid headache
            if self.isSliding:
                moveSquares = self.generate_slide()
            elif self.type == 'p':
                moveSquares = self.generate_pawn_move()
            else:
                moveSquares = self.generate_knight_move()
        return moveSquares
            
    def generate_legal_moves(self):  # generates moves for any piece regardless of type 
        moveSquares = self.generate_moves()
        opponentMoves = []
        finalSquares = []
        
        for s in moveSquares:
            self.move_hypothetical(s[0], s[1])
            kingLocation = findpiece('k', self.color)
            for p in pd.HYP_DIRECTORY:
                if pd.HYP_DIRECTORY[p] != None:
                    moves = pd.HYP_DIRECTORY[p].all_moves()
                    # print(moves)  # test
                    opponentMoves.extend(moves)
            pd.HYP_DIRECTORY = copy(pd.DIRECTORY)  # assign hypothetical back to normal every time
            pd.HYP_TURN = pd.TURN  # resets the turn
            if kingLocation not in opponentMoves:  # only accept the move if king won't be taken next turn
                finalSquares.append(s)
        return finalSquares

    
    # def possiblemoves(self, dir="N", by=1, knight=False):
        
    #     if not knight:
    #         super().move(self, horizontal=MOVEDIRS[dir][0], vertical=MOVEDIRS[dir][1])
# creating specific pieces that inherit from piece class
# class pawn(piece) ---------------------------------------
class pawn(Piece):
    CanTakeLeft = False
    CanTakeRight = False
    def __init__(self, color, file=0, rank=0):
        super().__init__(color, type="p", file=file, rank=rank)  # have to keep it like this for the defaults to work!
        self.type = "p"
    # def legalmoves(self):
    #     self.moves = []
    #     # if king will not be in check after piece moves
    #     #   if there is no piece in way of the current piece
    #     #       then move the piece
    #     # grab the file of the piece
    #     # l = numtoletter(self.file, self.rank)[0]
    #     # if piece is black:
    #     if self.color == "b":
    #         self.moves.append((self.file , self.rank - 1))
    #         if self.rank == 6:
    #             self.moves.append((self.file, self.rank - 2))
    #         # if self.CanTakeLeft:
    #         #     self.moves.append((l-1, self.rank - 1))
    #         # if self.CanTakeRight:
    #         #     self.moves.append((l+1, self.rank - 1))
    #     else:
    #         self.moves.append((self.file, self.rank + 1))
    #         if self.rank == 1:
    #             self.moves.append((self.file, self.rank + 2))
    #         # if self.CanTakeLeft:
    #         #     self.moves.append((l-1, self.rank + 1))
    #         # if self.CanTakeRight:
    #         #     self.moves.append((l+1, self.rank + 1))

        # print(f"my legal moves are {self.moves}")

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

# testpiece = queen('w', 0, 1)
# print(testpiece.rank)
# testpiece.legalmoves()
# print(testpiece.moves)
# testpiece2 = pawn('w', 2, 1)
# testpiece2.legalmoves()
# print(testpiece2.moves)