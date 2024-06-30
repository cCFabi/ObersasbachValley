import pygame
from map import check_collision
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill((255, 0, 0))  # Red square for the player
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed

    def update(self, keys, tmx_data):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        # Move player and check collisions
        self.rect.x += dx
        if check_collision(self.rect, tmx_data):
            self.rect.x -= dx
        self.rect.y += dy
        if check_collision(self.rect, tmx_data):
            self.rect.y -= dy
