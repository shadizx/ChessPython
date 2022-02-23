import pygame
import os

# constants
WIDTH, HEIGHT = 500, 500                       # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window

# function needed for refreshing window
def redrawwindow():
    pygame.display.update()

def main():
    # running main window
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

main()