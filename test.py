import pygame
pygame.init()
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()

counter, text = 180, '3:00'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.USEREVENT: 
            secondsHolder = ""
            counter -= 1
            minute = counter // 60
            seconds = counter % 60
            if seconds < 10:
                secondsHolder = "0"
            out = f"{minute}:{secondsHolder}{seconds}"
            text = str(out).rjust(3)
        if e.type == pygame.QUIT: 
            run = False

    screen.fill((255, 255, 255))
    screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
    pygame.display.flip()
    clock.tick(60)