import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from camera import Camera
from map import draw_map, check_collision
from menu import Menu
import settings

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Tiled Map Viewer")

# Load tiled map
tmx_data = load_pygame(settings.MAP_PATH)

# Set up the camera
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight
camera = Camera(map_width, map_height)

# Set up the player
player_pos = [screen.get_width() / 2, screen.get_height() / 2]
player = Player(player_pos, settings.PLAYER_SPEED)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Set up the menu
menu = Menu(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

# Main loop
running = True
in_menu = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if in_menu:
        in_menu = not menu.update(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
        menu.draw(screen)
    else:
        keys = pygame.key.get_pressed()
        player.update(keys, tmx_data)
        camera.update(player)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw the map
        draw_map(tmx_data, screen, camera)

        # Draw the player
        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(settings.FPS)

# Clean up
pygame.quit()
