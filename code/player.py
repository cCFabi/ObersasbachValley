import pygame as pg

class Player:
    def __int__(self):
        self.img = pg.image.load("").convert_alpha()
import pygame
from player import  Player
from pygame.locals import *


class Camera:
    def __init__(self, player):
        self.player = player
        self.window_size = pygame.display.get_window_size()
        self.scroll = pygame.Vector2(0, 0)

    def update(self):
        # Smooth camera follow
        self.scroll.x += (self.player.pos.x - self.scroll.x - (
                    self.window_size[0] / 2) + self.player.img.get_width() / 2) / 20
        self.scroll.y += (self.player.pos.y - self.scroll.y - (
                    self.window_size[1] / 2) + self.player.img.get_height() / 2) / 20

    def apply(self, entity):
        return entity.pos - self.scroll

    def draw(self, screen):
        player_pos = self.apply(self.player)
        screen.blit(self.player.img, player_pos)


# Main game loop example
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    player = Player(400, 300)
    camera = Camera(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))

        player.update(screen)
        camera.update()
        camera.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
