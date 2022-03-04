import pygame

# --- constants --- (UPPER_CASE names)
width = height = 640                           # constant width and height, set for basic testing
win = pygame.display.set_mode((width, height)) # setting window width and height
pygame.display.set_caption("SelfChessAI")      # setting name of window
fps = 60                                       # setting fps of game
dimension = width//8                           # dimension of each square
piece_size = int(dimension * 0.9)              # adjust the size of pieces on the board
piecedrag = False
offset = (dimension-piece_size)//2


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 120

# --- classses --- (CamelCase names)

# empty

# --- functions --- (lower_case names)

# empty

# --- main ---

# - init -

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("Tracking System")

# - objects -

piece = pygame.image.load("assets/" + "w" + "p" + ".png")

rectangle_draging = False

def drawmoves(surface, color, center, radius):
    place = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    surf = pygame.Surface(place.size, pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surface.blit(surf, place)

circlex = 40
circley = -40
circler = 20

# - mainloop -

clock = pygame.time.Clock()

running = True
x = 0
y = 0

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos

                    # x = (dimension * 3 + offset - 3)
                    # y = (height - dimension * (3 + 1) + offset - 3)
                    x = mouse_x - 78/2
                    y = mouse_y - 78/2

                    drawmoves(screen, (0, 0, 0, 127), (x, y), circler)
                    pygame.display.flip()

                    

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                x = mouse_x - 78/2
                y = mouse_y - 78/2

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)

    screen.blit(piece, ((dimension * 3 + offset - 3) + x , (height - dimension * (3 + 1) + offset - 3) + y))


    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()