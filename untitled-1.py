import pygame
import sys


def main():
    # инициализация Pygame:
    pygame.init()
    # размеры окна: 
    size = width, height = 800, 600
    # screen — холст, на котором нужно рисовать:
    successes, failures = pygame.init()
    print("{0} successes and {1} failures".format(successes, failures))
    
    
    screen = pygame.display.set_mode((720, 480))
    clock = pygame.time.Clock()
    FPS = 960 # Frames per second.
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    # RED = (255, 0, 0), GREEN = (0, 255, 0), BLUE = (0, 0, 255).
    
    rect = pygame.Rect((0, 0), (32, 32))
    image = pygame.Surface((32, 32))
    image.fill(WHITE)  
    
    while True:
        clock.tick(FPS)
        rect.move_ip(x, y)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_w, pygame.K_UP]:
                    x, y = 0, -1
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    x, y = 0, 1
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    x, y = -1, 0
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    x, y = 1, 0
    
        screen.fill(BLACK)
        screen.blit(image, rect)
        pygame.display.update()  # Or pygame.display.flip()

main()
quit()