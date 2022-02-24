import pygame
import os

#import piece images
# wPawn = pygame.image.load(os.path.join('assets/pieces', 'wP.png'))

# general piece class for all pieces
class Piece:
    # default constructor
    def __init__(self, color, type, hasmoved): 
        self.color = color
        self.selected = False # if piece is selected
        self.hasmoved = False

    def loadself(self):
        piece = pygame.transform.scale(pygame.image.load("assets/pieces" + self.color + self.type + ".png"))

    
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
    pass

class bishop(Piece):
    pass

class knight(Piece):
    pass

class rook(Piece):
    def __init__(self, color, type, hasmoved):
        super().__init__(color, type, hasmoved)
        self.type = "r"
        self.hasmoved = hasmoved

    def load(self):
        pass



class queen(Piece):
    pass

class king(Piece):
    pass