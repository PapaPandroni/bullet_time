from constants import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = SCREEN
        self.offset = pygame.Vector2()
   
    #this is basically our camera. redrawing the world depending on where the player position is. 
    def draw(self, target_pos):
        self.offset.x = - (target_pos[0] - SCREEN_WIDTH / 2)
        self.offset.y = - (target_pos[1] - SCREEN_HEIGHT / 2)
        
        #This is for smoother collisions. create overlap so the player can be behind or infront of a tree
        ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, "ground")]

        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery): #sort by centery to determine of player is infront or behind object
                self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
