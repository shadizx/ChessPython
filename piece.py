import pygame
import os

#import piece images
# wPawn = pygame.image.load(os.path.join('assets/pieces', 'wP.png'))

# general piece class for all pieces
class Piece:
    # default constructor
    def __init__(self, color, type, row = 0, col = 0): 
        self.color = color
        self.selected = False # if piece is selected
        self.hasmoved = False
        self.type = ""
        self.img = pygame.image.load("assets/pieces/" + color + type + ".svg")
    
    # moving a piece
    def move(self):
        pass

    # checking if a piece is selected
    def isSelected(self):
        return self.selected
    
    # printing a piece on the board
    def draw(self):
        pass
# class piece


# creating specific pieces that inherit from piece class
class pawn(Piece):
    def __init__(self, color, type = "p"):
        super().__init__(color, type = "p")
        self.type = "p"

class bishop(Piece):
    def __init__(self, color, type = "b"):
        super().__init__(color, type = "b")
        self.type = "b"

class knight(Piece):
    def __init__(self, color, type = "n"):
        super().__init__(color, type = "n")
        self.type = "n"

class rook(Piece):
    def __init__(self, color, type = "r"):
        super().__init__(color, type = "r")
        self.type = "r"

class queen(Piece):
    def __init__(self, color, type = "q"):
        super().__init__(color, type = "q")
        self.type = "q"

class king(Piece):
    def __init__(self, color, type = "k"):
        super().__init__(color, type = "k")
        self.type = "k"

class FEN:
    def __init__(self):
        self.fen =""
        #lowercase = black, upper = white
        self.startfen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.piecelist = {'p': pawn("b"),   'n': knight("b"),
                    'b': bishop("b"), 'r': rook("b"),
                    'q': queen("b"),  'k': king("b"),
                    'P': pawn("w"),   'N': knight("w"),
                    'B': bishop("w"), 'R': rook("w"),
                    'Q': queen("w"),  'K': king("w")}

        
        
    def LoadFromFEN(self):
        piecedict = {}
        squarelist = []
        letterlist = ["a","b","c","d","e","f","g","h"]
        splitfen = self.fen.split(' ')
        file = 0
        row = 7
        for s in splitfen[0]: #loop through the first string
            if s == "/":
                row -= 1
            elif s in range(9):
                file += 1
            else:
                temppiece = self.piecelist[s]

                
