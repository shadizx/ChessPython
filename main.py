# game.py
# responsible for running the main program
import pygame
import piece
import board

###################### constants ############################
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 120                                      # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
BOARD = board.Board()
piecedrag = False
# circle dimensions for showing legal moves
circlex = 40
circley = -40
circler = 20
# available legal moves
movesavail = []
##############################################################
# piece directory
# start of with directory of starting pieces
DIRECTORY = BOARD.LoadFromFEN()
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
    for square in BOARD.boardColors:
        square.draw()
    for m in movesavail:
        win.blit(m[0], m[1])
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    for i in range(64):
        if DIRECTORY[i] != None:
            DIRECTORY[i].draw()
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
        #load the legal moves on the board
        circleimg = circlemoves(win, (0, 0, 0, 127), (dimension * move[0] + circlex, height-dimension*(move[1]) + circley), circler)
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
# piecedisappear()
# clears the static location of a piece
def piecedisappear(p):
    tuplekey = piece.numtoletter(p.file, p.rank)
    sqtobecleared = BOARD.SquareDict[(tuplekey[0], int(tuplekey[1]))]
    drawboard()
    drawpieces()
    sqtobecleared.draw()   
###################################################################
# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True

    refresh()
    PIECECLICKED = False
#################################while loop####################################################
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if program is executed
                run = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1: # if left-clicked
            #         #get mouse pos
            #         xpos = getmpos()[0]
            #         ypos = getmpos()[1]
            #         # check if there is a piece where the mouse has been clicked
            #         if (pd.DIRECTORY[piece.numtoletter(xpos, ypos)] != None):
            #             # PIECEDRAG = True
            #             PIECECLICKED = True
            #             # grab the piece that is on that square
            #             p = pd.DIRECTORY[piece.numtoletter(xpos, ypos)]
            #             # print moves:
            #             printmoves(p)
            #             # clear the old static piece
            #             piecedisappear(p)
            #             # get mouse position
            #             xloc = event.pos[0]
            #             yloc = event.pos[1]
            #             # need to check if mouse is going out of the window, then let go of piece
            #             piece2mouse(xloc, yloc, p)
            #         else:
            #             # if clicked on board, remove available moves and refresh board
            #             movesavail.clear()
            #             refresh()
            # elif event.type == pygame.MOUSEBUTTONUP: # if mouse is unclicked
            #     if event.button == 1:
            #         if PIECECLICKED: # if previously clicked on piece
            #             # need to check if dropped on a legal move, then place the piece there
            #             x = getmpos()[0]
            #             y = getmpos()[1]
                        
            #             tobemoved = False # see if it is able to move to that square

            #             for move in p.moves:
            #                 if ((x,y) == move): # if available move is found save coords
            #                     tobemoved = True
            #                     newx = x
            #                     newy = y
            #             if tobemoved:
            #                 pd.DIRECTORY[piece.numtoletter(xpos, ypos)].move(newx,newy)
            #                 movesavail.clear()
            #             refresh()
            #             PIECECLICKED = False
            # elif pygame.mouse.get_pressed()[0] & PIECECLICKED: # while holding the piece
            #     # make the piece dissapear from it's previous place:
            #     piecedisappear(p)
            #     # get mouse position
            #     xloc = event.pos[0]
            #     yloc = event.pos[1]
            #     # need to check if mouse is going out of the window, then let go of piece
            #     if  xloc >= width - 1  or \
            #         yloc >= height - 1 or \
            #         xloc <= 1 or yloc <= 1:
            #             movesavail.clear()
            #             refresh()
            #             break
            #     else:
            #         # move piece to mouse
            #         piece2mouse(xloc, yloc, p)
#################################while loop####################################################
        
    pygame.quit()

if __name__ == "__main__":
    main()