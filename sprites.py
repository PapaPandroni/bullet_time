import pygame
from constants import *
from math import atan2, degrees

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

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, Groups):
        #player connection for the gun
        self.player = player
        self.distance = 140
        self.player_direction = pygame.math.Vector2(1,0)

        #sprite
        super().__init__(Groups)
        self.gun_surf = pygame.image.load(os.path.join("assets", "images", "gun", "gun.png")).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
            mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos()) #gets the mouse position and passes the x and y into a vector2
            player_pos = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2) #player is always in the center of the screen
            self.player_direction = (mouse_pos - player_pos).normalize() #vector math. 

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y) - 90) #atan2 gets the angle of a triangle from the two sides. in this case from the player and to the mouse
        
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1) #rotate the image from the original surf. not the self.image because of degradation
        else:
             self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1) #rotate the image from the original surf. not the self.image because of degradation
             self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)

        self.direction = direction
        self.speed = 1200
        
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000
    

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__ (self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player

        #create image
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.animation_speed = 6

        #rect
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        
        self.direction = pygame.Vector2()
        self.speed = 350

        #timer
        self.death_time = 0
        self.death_duration = 400

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
    
    def move(self, dt):
        #get direction
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize()

        #update rect pos + collision logic
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
    def destroy(self):
        #start a timer
        self.death_time = pygame.time.get_ticks()
        #change the image
        surf = pygame.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey("black")
        self.image = surf

    def death_timer(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def update(self, dt):
        if self.death_time == 0:
            self.move(dt)
            self.animate(dt)
        else:
            self.death_timer()
        