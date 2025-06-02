import pygame
from constants import *
from player import Player
from sprites import *
from groups import AllSprites

from pytmx.util_pygame import load_pygame #for the tiled map file
from random import randint


class Game(): #our basic game loop
    
    def __init__(self):
        #setup
        pygame.init()
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.ALL_SPRITES = AllSprites()
        self.COLLISION_SPRITES = pygame.sprite.Group()

        self.setup()

        
        

    def setup(self):
            map = load_pygame(os.path.join("assets", "data", "maps", "world.tmx")) #loading map
            #Loading layers of the map (objects, collisions, background and so on)
            for x,y,image in map.get_layer_by_name("Ground").tiles():
                Sprite((x*TILE_SIZE,y*TILE_SIZE), image, self.ALL_SPRITES)
            for obj in map.get_layer_by_name("Objects"):
                CollisionSprites((obj.x, obj.y), obj.image, (self.ALL_SPRITES, self.COLLISION_SPRITES))
            for obj in map.get_layer_by_name("Collisions"):
                wall = pygame.Surface((obj.width, obj.height))
                CollisionSprites((obj.x, obj.y), wall, self.COLLISION_SPRITES)
            #"special" layer for example spawnpoints
            for obj in map.get_layer_by_name("Entities"):
                if obj.name == "Player":
                    self.player=Player(PLAYER_IMAGE, (obj.x, obj.y), self.ALL_SPRITES, self.COLLISION_SPRITES)
            

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
            self.ALL_SPRITES.draw(self.player.rect.center)

            pygame.display.update()
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()