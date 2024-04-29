import pygame
from pygame.math import Vector2


class Player:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)
        self.speed = 5

    def move(self, keys):
        direction = Vector2(0, 0)
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1

        if direction.length() > 0:
            direction.normalize_ip()
            self.pos += direction * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.pos.x), int(self.pos.y)), 20)

    def

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

player = Player(400, 300)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    screen.fill((255, 255, 255))
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
