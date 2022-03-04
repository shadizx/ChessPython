import pygame

# --- constants --- (UPPER_CASE names)

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

rectangle = pygame.rect.Rect(300,300,164,164)
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

while running:

    # - events -

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:            
                if rectangle.collidepoint(event.pos):
                    rectangle_draging = True
                    mouse_x, mouse_y = event.pos
                    print(str(rectangle.x) + str(rectangle.y))
                    print(str(event.pos[0]) + str(event.pos[1]))

                    offset = 1/2 * 164

                    rectangle.x = mouse_x - 82
                    rectangle.y = mouse_y - 82

                    drawmoves(screen, (0, 0, 0, 127), (rectangle.x, rectangle.y), circler)
                    pygame.display.flip()

                    

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:            
                rectangle_draging = False

        elif event.type == pygame.MOUSEMOTION:
            if rectangle_draging:
                mouse_x, mouse_y = event.pos
                rectangle.x = mouse_x - 82
                rectangle.y = mouse_y - 82

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, rectangle)

    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

# - end -

pygame.quit()