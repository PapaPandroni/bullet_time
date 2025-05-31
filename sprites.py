import pygame
from constants import *

class CollisionSprites(pygame.sprite.Sprite):
    def __init__(self, pos, size, Groups):
        super().__init__(Groups)
        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_frect(center = pos)