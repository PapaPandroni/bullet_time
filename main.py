import pygame
from constants import *
from player import Player
from sprites import *
from groups import AllSprites

from pytmx.util_pygame import load_pygame #for the tiled map file
from random import randint, choice


class Game(): #our basic game loop
    
    def __init__(self):
        #setup
        pygame.init()
        
        self.running = True
        self.clock = pygame.time.Clock()

        #groups
        self.ALL_SPRITES = AllSprites()
        self.COLLISION_SPRITES = pygame.sprite.Group()
        self.BULLET_SPRITES = pygame.sprite.Group()
        self.ENEMY_SPRITES = pygame.sprite.Group()
       #gun_time
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cd = 100

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)

        self.spawn_positions = []

        #audio
        self.music = pygame.mixer.Sound(os.path.join("assets", "audio", "music.wav"))
        self.shoot_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "shoot.wav"))
        self.shoot_sound.set_volume(0.4)
        self.impact = pygame.mixer.Sound(os.path.join("assets", "audio", "impact.ogg"))
        self.music.play(-1)


        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(os.path.join("assets", "images", "gun", "bullet.png")).convert_alpha()
        
        folders = list(os.walk(os.path.join("assets", "images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in os.walk(os.path.join("assets", "images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
                    full_path = os.path.join(folder_path, file_name)
                    print(full_path)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)
        
    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.ALL_SPRITES, self.BULLET_SPRITES))
            self.shoot_sound.play()
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > self.gun_cd:
                self.can_shoot = True

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
                    self.gun = Gun(self.player, self.ALL_SPRITES)
                else: 
                    self.spawn_positions.append((obj.x, obj.y))
            
        
    def bullet_collision(self):
        if self.BULLET_SPRITES:
            for bullet in self.BULLET_SPRITES:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.ENEMY_SPRITES, False, pygame.sprite.collide_mask)
                if collision_sprites:
                    self.impact.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()
                

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.ENEMY_SPRITES, False, pygame.sprite.collide_mask):
            self.running = False
            
    def run(self):

        while self.running:
            
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_event:
                    
                    Enemy(choice(self.spawn_positions), choice(list(self.enemy_frames.values())), (self.ALL_SPRITES, self.ENEMY_SPRITES), self.player, self.COLLISION_SPRITES)
                
                    
            
            #update game
            self.gun_timer()
            self.input()
            self.ALL_SPRITES.update(dt)
            self.bullet_collision()
            self.player_collision()
            
            #draw game
            SCREEN.fill("black")
            self.ALL_SPRITES.draw(self.player.rect.center)

            pygame.display.update()
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()