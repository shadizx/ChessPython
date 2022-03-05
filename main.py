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
fps = 120                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
BOARD = board.Board()
piecedrag = False
circlex = 40
circley = -40
circler = 20
###################################################################
# available legal moves
movesavail = []
# squares that need to be cleared:
clearsquare = None
###################################################################
# drawcircle
def circlemoves(surface, color, center, radius):
    place = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    surf = pygame.Surface(place.size, pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return (surf, place)
###################################################################
# drawboard()
# useful for drawing the board
def drawboard():
    for square in BOARD.SquareDict.values():
        square.draw()
    for m in movesavail:
        win.blit(m[0], m[1])
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    for p in BOARD.Pieces:
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
# printmoves
# returns the location of the piece clicked, null if no piece has been clicked
def printmoves(p):
    #refresh movesavail:
    movesavail.clear()
    #load moves
    p.legalmoves()
    # loop through legal moves to show each legal move
    for move in p.moves:
        # translate a tuple such as ('g', 2) to corresponding file and rank (7,1)
        fr = piece.tupletranslate(move)
        #load the legal moves on the board
        circleimg = circlemoves(win, (0, 0, 0, 127), (dimension * fr[0] + circlex, height-dimension*(fr[1]+1) + circley), circler)
        movesavail.append(circleimg)
###################################################################
# piece2mouse
# moves a piece image location to the center of the mouse
def piece2mouse(mousex, mousey, p):
    xloc = mousex - 78/2
    yloc = mousey - 78/2
    win.blit(p.img, (xloc, yloc))
    pygame.display.flip()
###################################################################
# refresh()
# refreshes the board
def refresh():
    drawboard()
    drawpieces()
    pygame.display.update()
###################################################################
# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    mainboard = board.Board()
    mainboard.LoadFromFEN()
    refresh()
    PIECEDRAG = False
#################################while loop####################################################
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if program is executed
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if left-clicked
                    #get mouse pos
                    x = getmpos()[0]
                    y = getmpos()[1]
                    # check if there is a piece where the mouse has been clicked
                    if (board.PIECESloc[piece.numtoletter(x, y)] != None):
                        PIECEDRAG = True
                        #grab the piece that is on that square
                        p = board.PIECESloc[piece.numtoletter(x, y)]
                        # #print moves:
                        printmoves(p)
                        refresh()
            elif event.type == pygame.MOUSEBUTTONUP: # if mouse is unclicked
                if event.button == 1:
                    PIECEDRAG = False
                    refresh()
            elif pygame.mouse.get_pressed()[0] & PIECEDRAG: # while holding the piece
                # make the piece dissapear from it's previous place:
                tuplekey = piece.numtoletter(p.file, p.rank)
                sqtobecleared = BOARD.SquareDict[(tuplekey[0], int(tuplekey[1]))]
                drawboard()
                drawpieces()
                sqtobecleared.draw()
                # get mouse position
                xloc = event.pos[0]
                yloc = event.pos[1]
                # need to check if mouse is going out of the window, then let go of piece
                if  xloc >= width - 1  or \
                    yloc >= height - 1 or \
                    xloc <= 1 or yloc <= 1:
                        print("REACHED BORDER")
                        movesavail.clear()
                        refresh()
                        PIECEDRAG = False
                        break
                else:
                    # move piece to mouse
                    piece2mouse(event.pos[0], event.pos[1], p)
#################################while loop####################################################
        
    pygame.quit()

if __name__ == "__main__":
    main()