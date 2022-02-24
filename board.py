import pygame
import os
import piece

# constants
WIDTH, HEIGHT = 640, 640                   # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game

DIMENSION = WIDTH/8


class Square:
    # default constructor
    WHITE=(248,220,180)
    BLACK=(184,140,100)
    
    def __init__(self, file, rank, color): 
        self.file = file
        self.rank = rank
        self.isWhite = color
        self.color = self.WHITE if self.isWhite else self.BLACK

    #occupant:piece.Piece = None

    def draw(self):
        pygame.draw.rect(WIN, self.color, pygame.Rect((DIMENSION*(self.rank)), (HEIGHT-DIMENSION*(self.file+1)), DIMENSION, DIMENSION))
        # if self.occupant is not None:
        #     pygame.blit()  # TODO finish this with occupant class's png and position of the piece on board + a certain number of squares

StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# PIECES_DICT = {'p': piece.pawn(),   'n': piece.knight(),
#                'b': piece.bishop(), 'r': piece.rook(),
#                'q': piece.queen(),  'k': piece.king()}
class Board:
    # FEN = StartFEN
    def __init__(self):
        self.squaredict = {}
        self.squarelist = []
        self.letterlist = ["a","b","c","d","e","f","g","h"]
        self.numlist = [1,2,3,4,5,6,7,8]
        for indexf, l in enumerate(self.letterlist):
            for indexr, n in enumerate(self.numlist):
                isWhite = (indexf + indexr) % 2 != 0
                temp = Square(indexf, indexr, isWhite)
                self.squaredict[(l, n)] = temp
                self.squarelist.append(temp)
                
    # def load_position_from_fen(self):  # loads piece positions from the FEN
    #     FEN_SPLIT = self.FEN.split(' ')
    #     file = 0 
    #     rank = 7
    #     for s in FEN_SPLIT[0]:  # place pieces in their respective positions
    #         if s == '/':
    #             file = 0
    #             rank -= 1
    #         elif s in range(9):
    #             file += s
    #         else:
    #             self.squaredict[(self.letterlist[file], self.numlist[rank])].occupant = PIECES_DICT[s]
    #             file += 1

    def drawboard(self):
        for square in self.squarelist:
            square.draw()        






# function needed for refreshing window
def drawboard():
    mainboard = Board()
    mainboard.draw()
    pygame.display.update()