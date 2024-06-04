import pygame as pg
from pygame.math import Vector2

class Player:
    def __init__(self, x, y):
        self.img = pg.transform.scale(pg.image.load("assets/player.png"), (100, 100))
        self.pos = Vector2(x, y)
        self.neupos = Vector2(0, 0)
        self.speed = 5

    def walk(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.neupos.x = -1
        elif keys[pg.K_d]:
            self.neupos.x = 1
        else:
            self.neupos.x = 0

        if keys[pg.K_w]:
            self.neupos.y = -1
        elif keys[pg.K_s]:
            self.neupos.y = 1
        else:
            self.neupos.y = 0

        if self.neupos.length() > 0:
            self.neupos.normalize_ip()
            self.pos += self.neupos * self.speed

    def draw(self, screen):
        # pg.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), 20)
        screen.blit(self.img, self.pos)

    def update(self,screen):
        self.walk()
        self.draw(screen)