import pygame
from constants import *


pygame.init()
clock = pygame.time.Clock()



running = True
while running:
    
    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig = False
    
    SCREEN.fill("black")

    #game

    pygame.display.flip()

pygame.quit()


