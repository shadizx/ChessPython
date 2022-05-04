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
DIRECTORY = BOARD.pieceList
piecedrag = False
# circle dimensions for showing legal moves
circlex = 40
circley = -40
circler = 20
# available legal moves
movesavail = [] # why did we need this again?
turn_dict = {'w': (0, "white", "black"), 'b': (1, "black", "white")} # (bin, self, opponent) cosmetic, won't really need this later
##############################################################
# piece BOARD
# start of with BOARD of starting pieces
# BOARD = BOARD
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
    BOARD.draw()
    for m in movesavail:
        win.blit(m[0], m[1])
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    for i in BOARD.pieceList.values():
        if i is not None:
            i.draw()

###################################################################
# getmpos
# getting the    of the mouse upon clicking
def getmpos():
    pos = pygame.mouse.get_pos()
    x = pos[0] // 80
    y = 7 - pos[1] // 80
    return (x,y)
###################################################################
# printmoves
# returns the location of the piece clicked, null if no piece has been clicked
def printmoves(p, legalMoves):
    #refresh movesavail:
    movesavail.clear()
    # loop through legal moves to show each legal move
    if p.position in legalMoves:
        for move in legalMoves[p.position]:
            #load the legal moves on the board
            y, x = piece.getRankFile(move)
            circleimg = circlemoves(win, (0, 0, 0, 127), (dimension * x + (dimension/2), height - dimension * y - (dimension/2)), circler)  # TODO: check this
            movesavail.append(circleimg)
###################################################################
# piece2mouse
# moves a piece image location to the center of the mouse
def piece2mouse(mousex, mousey, p):
    xloc = mousex - piece.piece_size//2 - 3
    yloc = mousey - piece.piece_size//2 - 3
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
    sqtobecleared = BOARD.boardColors[p.position]
    drawboard()
    drawpieces()
    sqtobecleared.draw()   
###################################################################
# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    legalMoves = BOARD.generateLegalMoves(BOARD.turn)

    refresh()
    PIECECLICKED = False
#################################while loop####################################################
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if program is executed
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if left-clicked
                    #get mouse pos
                    xpos = getmpos()[0]
                    ypos = getmpos()[1]
                    pos = 8 * ypos + xpos
                    # check if there is a piece where the mouse has been clicked
                    if (pos in BOARD.pieceList):
                        PIECECLICKED = True
                        # grab the piece that is on that square
                        p = BOARD.pieceList[pos]
                        # if p.color == BOARD.turn:
                        # print moves:
                        printmoves(p, legalMoves)
                        # clear the old static piece
                        piecedisappear(p)
                        # get mouse position
                        xloc = event.pos[0]
                        yloc = event.pos[1]
                        # need to check if mouse is going out of the window, then let go of piece
                        piece2mouse(xloc, yloc, p)
                    else:
                        # if clicked on board, remove available moves and refresh board
                        movesavail.clear()
                        refresh()
            elif event.type == pygame.MOUSEBUTTONUP: # if mouse is unclicked
                if event.button == 1:
                    if PIECECLICKED: # if previously clicked on piece
                        # need to check if dropped on a legal move, then place the piece there
                        x = getmpos()[0]
                        y = getmpos()[1]
                        pos = 8 * y + x
                        
                        # check if we can even move there:
                        if p.position in legalMoves and p.color == BOARD.turn:
                            for move in legalMoves[p.position]:
                                if (move == pos): # if a legal move position is the same as pos
                                    # MOVE THE PIECE
                                    BOARD.makeMove(p.position, move)
                                    # generate new moves for the new board
                                    legalMoves = BOARD.generateLegalMoves(BOARD.turn)
                                    movesavail.clear()
                                    print("on move", BOARD.moveCounter)
                                    print("move list is " + str(BOARD.moveList))
                                    # TODO: make color changes upon check (optional)
                                    for pos in BOARD.pieceList:
                                        if BOARD.pieceList[pos].type == 'k' and BOARD.pieceList[pos].color == BOARD.turn:
                                            kingpos = pos
                                    if BOARD.squareIsThreatened(kingpos):
                                        if len(legalMoves) == 0:
                                            print(f"checkmate! {turn_dict[BOARD.turn][2]} wins!")
                                        else:
                                            print("check!")
                                    elif len(legalMoves) == 0:
                                        print("stalemate!")
                        refresh()
                        PIECECLICKED = False
            elif pygame.mouse.get_pressed()[0] & PIECECLICKED: # while holding the piece
                # make the piece dissapear from it's previous place:
                piecedisappear(p)
                # get mouse position
                xloc = event.pos[0]
                yloc = event.pos[1]
                # need to check if mouse is going out of the window, then let go of piece
                if  xloc >= width - 1  or \
                    yloc >= height - 1 or \
                    xloc <= 1 or yloc <= 1:
                        movesavail.clear()
                        refresh()
                        break
                else:
                    # move piece to mouse
                    piece2mouse(xloc, yloc, p)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    BOARD.revertMove()
                    # BOARD.generateMoves()
                    movesavail.clear()
                    refresh()
                elif event.key == pygame.K_RIGHT:
                    if (len(BOARD.unmadeMoves) > 0):
                            BOARD.makeMove(BOARD.unmadeMoves[-1][0], BOARD.unmadeMoves[-1][1])
                            BOARD.unmadeMoves.pop()
                            # BOARD.generateMoves()
                            movesavail.clear()
                            refresh()

#################################while loop####################################################
        
    pygame.quit()

if __name__ == "__main__":
    main()