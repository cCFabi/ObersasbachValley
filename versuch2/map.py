import pygame
import pytmx

def draw_map(tmx_data, screen, camera):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, camera.apply(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)))

def check_collision(player_rect, tmx_data):
    visible_layers = list(tmx_data.visible_layers)  # Convert generator to list
    for layer in visible_layers[2:]:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if gid != 0:
                    tile_rect = pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)
                    if player_rect.colliderect(tile_rect):
                        return True
    return False

