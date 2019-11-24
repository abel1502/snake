import pygame
import sys
import maths


def main():
    pygame.init()
    size = width, height = 800, 600
    
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    maxFps = 1000
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    image = pygame.Surface((32, 32))
    image.fill(WHITE)
    rect = image.get_rect()
    
    velocity = 0.25
    moveDir = maths.Vector2(1, 0)
    pos = maths.Vector2(0, 0)
    while True:
        deltaTime = clock.tick(maxFps)
        pos += moveDir * velocity * deltaTime
        pos = pos.clamp(screen.get_rect())
        rect.x, rect.y = round(pos).tuple()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    moveDir = maths.Vector2(0, -1)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    moveDir = maths.Vector2(0, 1)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    moveDir = maths.Vector2(-1, 0)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    moveDir = maths.Vector2(1, 0)
    
        screen.fill(BLACK)
        screen.blit(image, rect)
        pygame.display.update()

try:
    main()
finally:
    pygame.quit()