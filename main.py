import pygame
from constants import *
from player import Player


class Game():
    
    def __init__(self):
        #setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.ALL_SPRITES = pygame.sprite.Group()

        #sprites
        self.player=Player(PLAYER_IMAGE, self.ALL_SPRITES)

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