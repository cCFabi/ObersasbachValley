import pygame
import pytmx

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Tiled Map Viewer")

# Load tiled map
tmx_data = pytmx.load_pygame("design/Map.tmx")


def draw_map(tmx_data, screen):
    # Loop through all layers and tiles in the map
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the map
    draw_map(tmx_data, screen)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
