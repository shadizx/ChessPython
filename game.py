import pygame
import piece
import board
import os

WIDTH, HEIGHT = 640, 640                   # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game

# function needed for refreshing window
def drawwindow():
    # WIN.blit(board, (0,0))
    pygame.display.update()
    # pygame.draw.rect(WIN,BLUE,(200,150,100,50))



def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    mainboard = board.Board()
    mainboard.LoadFromFEN()
    mainboard.drawboard()
    rookp = piece.rook("b")
    WIN.blit(rookp.img, (320, 320))
    pygame.display.update()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main()