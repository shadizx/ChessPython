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
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)
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
# getmpos
# getting the position of the mouse upon clicking
def getmpos():
    pos = pygame.mouse.get_pos()
    x = pos[0] // 80
    y = 7 - pos[1] // 80
    return (x,y)
###################################################################
# piececlicked
# returns the location of the piece clicked, null if no piece has been clicked
def piececlicked():
    # get the mouse location
    x = getmpos()[0]
    y = getmpos()[1]
    # s = pygame.
       
    # check if there is a piece where the mouse has been clicked
    if (board.PIECESloc[board.numtoletter(x, y)] != None):
        draw_circle_alpha(win, (255, 0, 0, 127), (320, 320), 40)
        pygame.display.update()

        # pygame.draw.rect(win, (255, 0, 0, 127), pygame.Rect((dimension*(3)), (height-dimension*(3)), dimension, dimension))
        # pygame.draw.rec(win, )

    
    # return (x,y)
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
            if event.type == pygame.QUIT: # if program is executed
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if left-clicked on piece
                    x = getmpos()[0]
                    y = getmpos()[1]
                    print(board.numtoletter(x,y))
                    piececlicked()
                    
            if pygame.mouse.get_pressed()[0]: # while holding the piece
                try:
                    x = event.pos[0]
                    y = event.pos[1]
                    filex = x // 80
                    filey = y // 80
                    print("[" + str(filex) + ", " + str(filey) + "]")
                except AttributeError:
                    pass
                    # mainboard = board.Board()
                    # mainboard.LoadFromFEN()
                    # pieceimgs = board.Board()
                    # for p in pieceimgs.Pieces:
                    #     if p.rect.collidepoint(pos):
                    #         p.clicked = True

    pygame.quit()

if __name__ == "__main__":
    main()