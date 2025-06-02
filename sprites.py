import pygame
from constants import *

class Sprite(pygame.sprite.Sprite):
    def __init__ (self, pos, surf, Groups):
        super().__init__
        super().__init__(Groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)     
        self.ground = True

class CollisionSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, Groups):
        super().__init__(Groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)