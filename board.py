import pygame
import os

# constants
WIDTH, HEIGHT = 720, 720                     # constant width and height, set for basic testing   
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game

DIMENSION = WIDTH/8

class Square:
    # default constructor
    WHITE=(248,220,180)
    BLACK=(184,140,100)
    
    def __init__(self, file, rank, color): 
        self.file = file
        self.rank = rank
        self.isWhite = color
        self.color = self.WHITE if self.isWhite else self.BLACK

    def draw(self):
        pygame.draw.rect(WIN, self.color, pygame.Rect((DIMENSION*(self.rank)), (HEIGHT-DIMENSION*(self.file+1)), DIMENSION, DIMENSION))
        

# function needed for refreshing window
def drawwindow():
    for file in range(8):
        for rank in range(8):
            isWhite = (file+rank)%2 != 0
            Square(file, rank, isWhite).draw()
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
