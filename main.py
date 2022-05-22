# main.py
# responsible for running the main program
import pygame
import piece
import board
pygame.init()

###################### constants ############################
WIDTH, HEIGHT = 1200, 640                           # constant width and height, set for basic testing
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
FPS = 120                                      # setting fps of game
DIMENSION = HEIGHT//8                           # dimension of each square
piece_size = int(DIMENSION * 0.9)              # adjust the size of pieces on the board
BOARD = board.Board()
BACKGROUNDCOLOR = (22,21,17)
TIMERSQAURE = (37,36,32)
# circle dimensions for showing legal moves
circler = 20
# available legal moves
legalCircles = []
##################################################################
# class clock, responsible for each sides clock
class Clock:
    # game modes
    BULLET = board.BULLET
    BLITZ = board.BLITZ
    RAPID = board.RAPID
    CLASSICAL = board.CLASSICAL
    Timer = 0
    TimerText = ""

    def __init__(self, timeSeconds):
        # initiate timer
        self.Timer = timeSeconds
        # initiate timer with text format
        self.TimerText = self.secondsConvert(timeSeconds)
        self.font = pygame.font.SysFont('Consolas', 80)
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def secondsConvert(self, seconds):
        secondsHolder = minuteHolder = ""
        minute, seconds = seconds // 60, seconds % 60
        if minute < 10:
            minuteHolder = "0"
        if seconds < 10:
            secondsHolder = "0"
        out = f"{minuteHolder}{minute}:{secondsHolder}{seconds}".rjust(3)
        return out
    
    def tick(self):
        if self.Timer > 0:
            self.Timer -= 1
            self.TimerText = self.secondsConvert(self.Timer)
            
###################################################################
# times for games
timeFormat = 63
wTimer = Clock(timeFormat)
bTimer = Clock(timeFormat)
###################################################################
# drawcircles
# draws circles for legal moves of a piece
def drawCircles(surface, color, center, radius):
    place = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    surf = pygame.Surface(place.size, pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    return (surf, place)
###################################################################
# drawboard()
# useful for drawing the board
def drawboard():
    BOARD.draw()
    for circle in legalCircles:
        WIN.blit(circle[0], circle[1])
###################################################################
# drawpieces()
# useful for drawing the pieces
def drawpieces():
    for i in BOARD.pieceList.values():
        i.draw()
###################################################################
# getmpos
# getting the position of the mouse upon clicking
def getmpos():
    pos = pygame.mouse.get_pos()
    x = pos[0] // DIMENSION
    y = 7 - pos[1] // DIMENSION
    return (x,y)
###################################################################
# printmoves
def printmoves(p):
    #refresh legalCircles:
    legalCircles.clear()
    # loop through legal moves to show each legal move
    if p in BOARD.moveDict:
        for move in BOARD.moveDict[p]:
            #load the legal moves on the board
            y, x = piece.getRankFile(move)
            circleimg = drawCircles(WIN, (0, 0, 0, 127), (DIMENSION * x + (DIMENSION/2), HEIGHT - DIMENSION * y - (DIMENSION/2)), circler)
            legalCircles.append(circleimg)
###################################################################
# piece2mouse
# moves a piece image location to the center of the mouse
def piece2mouse(mousex, mousey, p):
    xloc = mousex - piece.piece_size//2 - 3
    yloc = mousey - piece.piece_size//2 - 3
    WIN.blit(p.img, (xloc, yloc))
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
# animateMove()
# does the animation for making a move
def animateMove(p, pos, PIECECLICKED = None):
    if p in BOARD.moveDict and p.color == BOARD.turn:
            for move in BOARD.moveDict[p]:
                if (move == pos): # if a legal move position is the same as pos
                    # MOVE THE PIECE
                    BOARD.makeMove(p.position, move)
                    # generate new moves for the new board
                    legalCircles.clear()
                    PIECECLICKED = False
###################################################################
# drawui()
# draws the ui
def drawUI():
    WIN.fill(BACKGROUNDCOLOR)
    pygame.draw.rect(WIN, TIMERSQAURE, pygame.Rect(680, 195, 480, 250))
    
    # black timer square
    pygame.draw.rect(WIN, TIMERSQAURE, pygame.Rect(680, 125, 219, 70))
    WIN.blit(bTimer.font.render(bTimer.TimerText, True, (255, 255, 255)), (680, 125))
    # white timer square
    pygame.draw.rect(WIN, TIMERSQAURE, pygame.Rect(680, 444, 219, 70))
    WIN.blit(wTimer.font.render(wTimer.TimerText, True, (255, 255, 255)), (680, 445)) 
###################################################################
# main driver
def main():
    # running main window
    clock = pygame.time.Clock()
    run = True

    drawUI()
    board.mixer.play('gameStart')
    refresh()

    PIECECLICKED = False
################################# while loop ####################################################
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # if program is executed
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # if left-clicked
                    # # # # # # # # # # # # # # # # # # # FOR TESTING PURPOSES: # # # # # # # # # # # # # # # # # # #
                    # print("\n\n######################################################################")
                    # print("movelist is ", str(BOARD.moveList))
                    print(f'annotations: {BOARD.annotationsList}')
                    # print("unmade moves is ", str(BOARD.unmadeMoves))
                    # print("PIECELIST", BOARD.pieceList)
                    # print("######################################################################")
                    # print("piecelist is ", BOARD.pieceList)
                    # print("checkdict is ", BOARD.checkDict)
                    # print(BOARD.inCheck)
                    # print("kings is ", str(BOARD.kings))
                    # print("line of check is ", BOARD.lineOfCheck)
                    # print("######################################################################")
                    # if BOARD.turn == "w":
                    #     print("white legal moves is ", str(BOARD.whiteReach))
                    # else:
                    #     print("black legal moves is ", str(BOARD.blackReach))

                    # print(str(BOARD.pinnedPieces))
                    # print(str(BOARD.whiteLegalMoves.keys()))
                    print('White Points: ', BOARD.whitePoints)
                    print('Black Points: ', BOARD.blackPoints)
                    # print('Total White Points: ', BOARD.totalWhitePoints)
                    # print('Total Black Points: ', BOARD.totalBlackPoints)
                    # # # # # # # # # # # # # # # # # # # FOR TESTING PURPOSES: # # # # # # # # # # # # # # # # # # #

                    # check if previously clicked on a piece to move the piece there
                    # this way, we can drag and click to move pieces
                    #get mouse pos
                    xpos = getmpos()[0]
                    ypos = getmpos()[1]
                    pos = 8 * ypos + xpos
                    
                    if PIECECLICKED:
                        animateMove(p, pos, PIECECLICKED)
                        
                    # check if there is a piece where the mouse has been clicked
                    if (pos in BOARD.pieceList):
                        PIECECLICKED = True
                        # grab the piece that is on that square
                        p = BOARD.pieceList[pos]
                        if p.color == BOARD.turn:
                            # print moves:
                            printmoves(p)
                            # clear the old static piece
                            piecedisappear(p)
                            # get mouse position
                            mousepos = pygame.mouse.get_pos()
                            xloc = mousepos[0]
                            yloc = mousepos[1]
                            # need to check if mouse is going out of the window, then let go of piece
                            piece2mouse(xloc, yloc, p)
                    if (pos not in BOARD.pieceList) or (BOARD.pieceList[pos].color != BOARD.turn):
                        # if clicked elsewhere, remove available moves and refresh board
                        PIECECLICKED = False
                        legalCircles.clear()
                        refresh()
            elif event.type == pygame.MOUSEBUTTONUP: # if mouse is unclicked
                if event.button == 1:
                    if PIECECLICKED: # if previously clicked on piece
                        # need to check if dropped on a legal move, then place the piece there
                        x = getmpos()[0]
                        y = getmpos()[1]
                        pos = 8 * y + x
                        
                        animateMove(p,pos)
                        refresh()
            elif pygame.mouse.get_pressed()[0] & PIECECLICKED: # while holding the piece
                # make the piece dissapear from it's previous place:
                piecedisappear(p)
                # get mouse position
                mousepos = pygame.mouse.get_pos()
                xloc = mousepos[0]
                yloc = mousepos[1]
                # need to check if mouse is going out of the window, then let go of piece
                if  xloc >= HEIGHT - 1  or \
                    yloc >= HEIGHT - 1 or \
                    xloc <= 1 or yloc <= 1:
                        legalCircles.clear()
                        drawUI()
                        refresh()
                        break
                else:
                    # move piece to mouse
                    piece2mouse(xloc, yloc, p)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    BOARD.revertMove()
                    legalCircles.clear()
                    PIECECLICKED = False
                    refresh()
                elif event.key == pygame.K_RIGHT:
                    if (len(BOARD.unmadeMoves) > 0):
                            BOARD.makeMove(BOARD.unmadeMoves[-1][0], BOARD.unmadeMoves[-1][1], True)
                            legalCircles.clear()
                            refresh()
            if event.type == pygame.USEREVENT:
                # for timer
                if BOARD.turn == "w":
                    wTimer.tick()
                    pygame.draw.rect(WIN, TIMERSQAURE, pygame.Rect(680, 444, 219, 70))
                    WIN.blit(wTimer.font.render(wTimer.TimerText, True, (255, 255, 255)), (680, 445))
                else:
                    bTimer.tick()
                    pygame.draw.rect(WIN, TIMERSQAURE, pygame.Rect(680, 125, 219, 70))
                    WIN.blit(bTimer.font.render(bTimer.TimerText, True, (255, 255, 255)), (680, 125))
                pygame.display.flip()
        

#################################while loop####################################################
        
    pygame.quit()

if __name__ == "__main__":
    main()