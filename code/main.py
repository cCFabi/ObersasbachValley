import sys
import pygame as pg
from player import Player
from editmode import EditMode
pg.init()
WIDTH = 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Obersasbach Valley')
clock = pg.time.Clock()
placed_rects = []
grid = 50

player = Player(WIDTH // 2, HEIGHT // 2)  # Create an instance of the Player class
edit = EditMode(screen, grid, placed_rects)
while True:
    screen.fill((0, 255, 0))  # Fill the screen with green color
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                # Toggel logic hier allso e = not e
                edit.edittoggle()

    for rect_pos in placed_rects:
        pg.draw.rect(screen, (139, 69, 19), (*rect_pos, grid, grid))
    player.update(screen)  # Call the update method of the Player instance
    pg.display.flip()
    clock.tick(120)