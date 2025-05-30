import pygame
import os
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, surf, Groups):
        super().__init__(Groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        #movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        
        #find direction
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        #update position
        self.rect.center += self.direction * self.speed * dt
    
    def update(self, dt):
        self.input()
        self.move(dt)

        #keep player in bound
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)