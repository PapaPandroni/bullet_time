import pygame
import os

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Time")

TILE_SIZE = 64

#Imports
PLAYER_IMAGE_PATH = os.path.join("assets", "images", "player", "down", "0.png")
PLAYER_IMAGE = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()

