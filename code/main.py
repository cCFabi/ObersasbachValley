import sys
import pygame as pg
from player import Player
from editmode import EditMode
from pygame.locals import *
from camera import Camera
#from taskleiste import Taskleiste

pg.init()
WIDTH = 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Obersasbach Valley')
clock = pg.time.Clock()
placed_rects = []
grid = 50
selector = False
player = Player(WIDTH // 2, HEIGHT // 2)  # Create an instance of the Player class
up = False
down = False
left = False
right = False
edit = EditMode(screen, grid, placed_rects)

camera = Camera(player)  # Initialize the Camera class with player, blocks, and window size

while True:
    screen.fill((0, 255, 0))  # Fill the screen with green color
    camera.update()  # Update the camera with player movement
    camera.draw(screen)  # Draw the camera view on the screen
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                selector = not selector

    if selector:
        edit.handle_event()

    for rect_pos in placed_rects:
        pg.draw.rect(screen, (139, 69, 19), (*rect_pos, grid, grid))

    player.update(screen)  # Call the update method of the Player instance
    pg.display.flip()
    clock.tick(120)