import pygame
from pygame.locals import *

class Camera:
    def __init__(self, player):
        self.player = player
        self.window_size = pygame.display.get_window_size()
        self.scroll = pygame.Vector2(0, 0)

    def update(self):
        # Smooth camera follow
        self.scroll.x += (self.player.pos.x - self.scroll.x - (self.window_size[0] / 2) + self.player.img.get_width() / 2) / 20
        self.scroll.y += (self.player.pos.y - self.scroll.y - (self.window_size[1] / 2) + self.player.img.get_height() / 2) / 20

    def apply(self, entity):
        return entity.pos - self.scroll

    def draw(self, screen):
        player_pos = self.apply(self.player)
        screen.blit(self.player.img, player_pos)

       #for block in self.blocks:
       #     scroll_block = block.copy()
       #     scroll_block.x = scroll_block.x - self.scroll[0]
       #     scroll_block.y = scroll_block.y - self.scroll[1]
       #     pygame.draw.rect(screen, (0, 0, 255), scroll_block)