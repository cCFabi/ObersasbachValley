import sys

import pygame as pg

pg.init()
a = 21 * 3
FAKTOR = 3
WIDTH = 1280
HEIGHT = 720
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Obersasbach Valley')
clock = pg.time.Clock()
selector = False
mov_x = 200
mov_y = 200
grid = 50
out = False
wspeed = 5
leisten_pos = [(WIDTH // 2 - 270, HEIGHT - 45), (WIDTH // 2 - 210, HEIGHT - 45), (WIDTH // 2 - 153, HEIGHT - 45),
               (WIDTH // 2 - 96, HEIGHT - 45), (WIDTH // 2 - 39, HEIGHT - 45), (WIDTH // 2 + 18, HEIGHT - 45),
               (WIDTH // 2 + 75, HEIGHT - 45), (WIDTH // 2 + 132, HEIGHT - 45), (WIDTH // 2 + 189, HEIGHT - 45),
               (WIDTH // 2 + 246, HEIGHT - 45)]


# wheat
# wheat_img = pg.image.load("Wheat.png")
wheat_img = pg.transform.scale(pg.image.load("wheat.png").convert_alpha(), (12 * 2, 13 * 2))

cursor_img = pg.image.load("cursor.png").convert_alpha()
pg.mouse.set_visible(False)
cursor_img_rect = cursor_img.get_rect()
# leiste = pg.image.load("menubar3.png")
leiste = pg.transform.scale(pg.image.load("menubar.png").convert_alpha(), (188 * FAKTOR, 16 * FAKTOR))
leiste_rect = leiste.get_rect()

placed_rects = []


def editmode():
    mouse_position = pg.mouse.get_pos()
    cell_x = mouse_position[0] // grid * grid
    cell_y = mouse_position[1] // grid * grid
    if pg.mouse.get_pressed()[0]:
        placed_rects.append((cell_x, cell_y))
    elif pg.mouse.get_pressed()[2]:  # Right click to delete the rectangle under the cursor
        for rect_position in placed_rects:
            if rect_position[0] == cell_x and rect_position[1] == cell_y:
                placed_rects.remove(rect_position)
    pg.draw.rect(screen, "blue", (cell_x, cell_y, grid, grid), 0)


def player():
    pg.draw.rect(screen, "red", (mov_x, mov_y, 50, 50))


while True:
    key = pg.key.get_pressed()
    screen.fill("green")

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                selector = not selector

    if selector:
        editmode()

    for rect_pos in placed_rects:
        pg.draw.rect(screen, (139, 69, 19), (*rect_pos, grid, grid))

    if key[pg.K_w]:
        mov_y -= wspeed
    if key[pg.K_s]:
        mov_y += wspeed
    if key[pg.K_a]:
        mov_x -= wspeed
    if key[pg.K_d]:
        mov_x += wspeed

    player()

    screen.blit(leiste, (WIDTH // 2 - 564 // 2, HEIGHT - 55))
    for i in range(len(leisten_pos)):
        screen.blit(wheat_img, leisten_pos[i])

    mouse_pos = pg.mouse.get_pos()
    if 0 <= mouse_pos[0] <= WIDTH and 0 <= mouse_pos[1] <= HEIGHT:
        cursor_img.set_alpha(255)
    else:
        cursor_img.set_alpha(0)

    cursor_img_rect.center = pg.mouse.get_pos()
    screen.blit(cursor_img, cursor_img_rect)

    pg.display.flip()
    clock.tick(120)
