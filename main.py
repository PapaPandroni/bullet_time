import pygame
from constants import *
from player import Player
from sprites import *

from random import randint


class Game():
    
    def __init__(self):
        #setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.ALL_SPRITES = pygame.sprite.Group()
        self.COLLISION_SPRITES = pygame.sprite.Group()

        #sprites
        self.player=Player(PLAYER_IMAGE, self.ALL_SPRITES, self.COLLISION_SPRITES)
        for i in range(6):
            x, y = randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)
            w,h = randint(60, 100), randint(50,100)
            CollisionSprites((x,y), (w,h), (self.ALL_SPRITES, self.COLLISION_SPRITES))

    def run(self):
    
        

        while self.running:
            
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #update game
            self.ALL_SPRITES.update(dt)
            
            #draw game
            SCREEN.fill("black")
            self.ALL_SPRITES.draw(SCREEN)

            pygame.display.update()
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()