import pygame
import os
from constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, surf, pos, Groups, collision_sprites):
        super().__init__(Groups)
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -90) 
        #movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 500

        #pass all the collision sprites to be able to check for collissions
        self.collision_sprites = collision_sprites 
        

    def load_images(self):
        self.frames = {"left": [], "right": [], "up": [], "down": []} #dictionary for all images pathes
        #important that state keys == folder names
        for state in self.frames.keys(): 
            for folder_path, subfolders, file_names in os.walk(os.path.join("assets", "images", "player", state)): #getting full path
                for file_name in sorted(file_names, key = lambda name: int(name.split(".")[0])):
                    full_path = os.path.join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.frames[state].append(surf) #appends the surfs to the dictionary
        


    def input(self):
        keys = pygame.key.get_pressed()
        
        #find direction
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #this is for not moving faster diagonally
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self, dt):
        #update position
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                
    def animate(self, dt):
        #get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"


        #basic animation
        #condition to only animate while moving
        self.frame_index = self.frame_index + 5 * dt if self.direction else 0 
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
    
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)


        #keep player in bound
        #self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        #self.pos = pygame.math.Vector2(self.rect.topleft)