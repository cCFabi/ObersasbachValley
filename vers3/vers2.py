import pygame
import sys
import pickle

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Simple Stardew Valley Clone')

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()

# Load images
character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (32, 32))
background_image = pygame.image.load('background.png')

class Character:
    def __init__(self, x, y):
        self.image = character_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.inventory = []

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

    def interact(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                obj.interact(self)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def add_to_inventory(self, item):
        self.inventory.append(item)
        print(f"Added {item} to inventory")

class Tile:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.interactable = False

    def interact(self, character):
        if self.interactable:
            character.add_to_inventory('item_from_tile')
            self.interactable = False

def create_map():
    tiles = []
    tile_size = 32
    for y in range(0, 600, tile_size):
        for x in range(0, 800, tile_size):
            tile = Tile(x, y, pygame.Surface((tile_size, tile_size)))
            tile.image.fill((0, 255, 0))
            tiles.append(tile)
    return tiles

class GameObject:
    def __init__(self, x, y, image, name):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.name = name

    def interact(self, character):
        character.add_to_inventory(self.name)

def create_game_objects():
    objects = []
    crop_image = pygame.Surface((32, 32))
    crop_image.fill((255, 0, 0))
    crop = GameObject(200, 200, crop_image, 'Crop')
    objects.append(crop)
    return objects

def save_game(filename, character, game_objects):
    with open(filename, 'wb') as f:
        pickle.dump((character, game_objects), f)
    print("Game saved!")

def load_game(filename):
    with open(filename, 'rb') as f:
        character, game_objects = pickle.load(f)
    print("Game loaded!")
    return character, game_objects

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.options = ["Resume", "Save", "Load", "Quit"]
        self.selected = 0

    def draw(self, screen):
        screen.fill((0, 0, 0))
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            screen.blit(text, (400 - text.get_width() // 2, 300 + i * 40 - text.get_height() // 2))

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(150)
        if keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(150)
        if keys[pygame.K_RETURN]:
            return self.options[self.selected]
        return None

def main():
    character = Character(400, 300)
    tiles = create_map()
    game_objects = create_game_objects()
    menu = Menu()
    in_menu = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            in_menu = True

        if in_menu:
            selected_option = menu.handle_keys()
            if selected_option == "Resume":
                in_menu = False
            elif selected_option == "Save":
                save_game('savefile.pkl', character, game_objects)
                in_menu = False
            elif selected_option == "Load":
                character, game_objects = load_game('savefile.pkl')
                in_menu = False
            elif selected_option == "Quit":
                pygame.quit()
                sys.exit()
            menu.draw(screen)
        else:
            screen.blit(background_image, (0, 0))

            character.handle_keys()
            character.interact(game_objects)
            for tile in tiles:
                screen.blit(tile.image, tile.rect.topleft)
            for obj in game_objects:
                screen.blit(obj.image, obj.rect.topleft)

            character.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
