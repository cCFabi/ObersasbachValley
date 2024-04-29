import pygame as pg
class EditMode:
    def __init__(self, screen, grid, placed_rects):
        self.screen = screen
        self.grid = grid
        self.placed_rects = placed_rects
        self.selector = False

    def handle_event(self):
        mouse_position = pg.mouse.get_pos()
        cell_x = mouse_position[0] // self.grid * self.grid
        cell_y = mouse_position[1] // self.grid * self.grid
        if pg.mouse.get_pressed()[0]:
            self.placed_rects.append((cell_x, cell_y))
        elif pg.mouse.get_pressed()[2]:
            for rect_position in self.placed_rects:
                if rect_position[0] == cell_x and rect_position[1] == cell_y:
                    self.placed_rects.remove(rect_position)
        pg.draw.rect(self.screen, "blue", (cell_x, cell_y, self.grid, self.grid), 0)

    def selection(self):
        if self.selector:
            self.handle_event()
            """for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        self.selector = not self.selector"""

    def draw(self):
        for rect_pos in self.placed_rects:
            pg.draw.rect(self.screen, (139, 69, 19), (*rect_pos, self.grid, self.grid))
