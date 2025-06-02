from constants import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = SCREEN
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        self.offset.x = - (target_pos[0] - SCREEN_WIDTH / 2)
        self.offset.y = - (target_pos[1] - SCREEN_HEIGHT / 2)
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
