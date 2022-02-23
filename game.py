import pygame
import os

# constants
WIDTH, HEIGHT = 500, 500                       # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game

board = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'board.png')), (500,500))

# function needed for refreshing window
def drawwindow():
    WIN.blit(board, (0,0))
    pygame.display.update()

def main():
    # running main window
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        drawwindow()
    pygame.quit()

main()