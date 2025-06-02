import pygame
from constants import *

#basic sprite that need to render. the background for example
class Sprite(pygame.sprite.Sprite):
    def __init__ (self, pos, surf, Groups):
        super().__init__
        super().__init__(Groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)     
        self.ground = True


#all sprites with collision
class CollisionSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, Groups):
        super().__init__(Groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)