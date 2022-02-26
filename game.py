# game.py
# responsible for running the main program

import pygame
import piece
import board
import os
from copy import copy, deepcopy

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
###################### constants ############################

##################################################################
# drawboard()
# useful for drawing the board
def drawboard():
    squareimgs = board.Board()
    for square in squareimgs.SquareDict.values():
        square.draw()
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    pieceimgs = board.Board()
    for p in pieceimgs.Pieces:
        p.draw()
###################################################################

# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    mainboard = board.Board()
    mainboard.LoadFromFEN()
    drawboard()
    drawpieces()
    pygame.display.update()

    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main()