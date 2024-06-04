import pygame as pg

class Taskleiste(pg.sprite.Sprite):
    def __init__(self, screen, image):
        self.image = image
        self.screen = screen
        self.width = pg.display.get_window_size()[0] #1280


    def