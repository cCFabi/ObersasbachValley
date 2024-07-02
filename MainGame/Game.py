import json
import os
import sys
import time

import pygame
from pytmx import load_pygame, TiledTileLayer

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
PLAYER_WIDTH, PLAYER_HEIGHT = int(172 / 2), int(124 / 2)
HITBOXVALUE = 4
GRID_SIZE = 16 * 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Obersasbach Valley')

clock = pygame.time.Clock()

debug = False


def load_character_images(direction):
    images = []
    for i in range(4):
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, 'character', direction, f'{i}.png')
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            images.append(image)
        except pygame.error:
            print(f"Warning: File '{path}' not found.")
    return images


animations = {
    'down': load_character_images('down'),
    'up': load_character_images('up'),
    'left': load_character_images('left'),
    'right': load_character_images('right')
}

base_path = os.path.dirname(__file__)
background_tmx = load_pygame(os.path.join(base_path, "UI", "GAMEMEM.tmx"))


def draw_map():
    scale_factor = 2
    for layer in background_tmx.visible_layers:
        if isinstance(layer, TiledTileLayer):
            for x, y, gid in layer:
                tile = background_tmx.get_tile_image_by_gid(gid)
                if tile:
                    tile = pygame.transform.scale(tile, (background_tmx.tilewidth * scale_factor,
                                                         background_tmx.tileheight * scale_factor))
                    screen.blit(tile, (x * background_tmx.tilewidth * scale_factor,
                                       y * background_tmx.tileheight * scale_factor))


def load_crop_images(folder):
    images = []
    for i in range(1, 6):
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, folder, f'{i}.png')
        try:
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (32, 32))
            images.append(image)
        except pygame.error:
            print(f"Warning: File '{path}' not found.")
    return images


crop_images = {
    'Wheat': load_crop_images('crops/Weizen/'),
    'Corn': load_crop_images('crops/Mais/'),
    'Tomato': load_crop_images('crops/Tomaten/')
}

crop_prices = {
    'Wheat': 10,
    'Corn': 15,
    'Tomato': 20
}

shop_items = {
    'Wheat Seed': 3,
    'Corn Seed': 5,
    'Tomato Seed': 7
}

popup_background = pygame.image.load(os.path.join(base_path, "other UI", "Menu.png")).convert_alpha()
popup_background = pygame.transform.scale(popup_background,
                                          (popup_background.get_width() * 3, popup_background.get_height() * 3))

popup_x = (SCREEN_WIDTH - popup_background.get_width()) // 2
popup_y = (SCREEN_HEIGHT - popup_background.get_height()) // 2


class Character:
    def __init__(self, x, y):
        self.animations = animations
        self.current_animation = self.animations['down']
        self.image_index = 0
        self.image = self.current_animation[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        bounding_rect = self.image.get_bounding_rect(min_alpha=1)
        self.hitbox = bounding_rect
        self.hitbox.center = self.rect.center
        self.hitbox.y += HITBOXVALUE
        self.speed = 5
        self.inventory = {}
        self.currency = 100
        self.moving = False
        self.frame_delay = 2.5
        self.frame_counter = 0
        self.messages = []
        self.walkable_layers = ['Gras', 'Boden']

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        self.moving = False
        original_rect = self.rect.copy()
        original_hitbox = self.hitbox.copy()

        if keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
            self.hitbox.move_ip(-self.speed, 0)
            self.current_animation = self.animations['left']
            if not self.check_collision(self.hitbox) and self.hitbox.left >= 0:
                self.moving = True
            else:
                self.rect = original_rect
                self.hitbox = original_hitbox

        if keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)
            self.hitbox.move_ip(self.speed, 0)
            self.current_animation = self.animations['right']
            if not self.check_collision(self.hitbox) and self.hitbox.right <= SCREEN_WIDTH:
                self.moving = True
            else:
                self.rect = original_rect
                self.hitbox = original_hitbox

        if keys[pygame.K_w]:
            self.rect.move_ip(0, -self.speed)
            self.hitbox.move_ip(0, -self.speed)
            self.current_animation = self.animations['up']
            if not self.check_collision(self.hitbox) and self.hitbox.top >= 0:
                self.moving = True
            else:
                self.rect = original_rect
                self.hitbox = original_hitbox

        if keys[pygame.K_s]:
            self.rect.move_ip(0, self.speed)
            self.hitbox.move_ip(0, self.speed)
            self.current_animation = self.animations['down']
            if not self.check_collision(self.hitbox) and self.hitbox.bottom <= SCREEN_HEIGHT:
                self.moving = True
            else:
                self.rect = original_rect
                self.hitbox = original_hitbox

        self.hitbox.center = self.rect.center
        self.hitbox.y += HITBOXVALUE

    def check_collision(self, rect):
        scale_factor = 2
        tile_size = background_tmx.tilewidth * scale_factor
        for layer in background_tmx.visible_layers:
            if hasattr(layer, 'properties') and layer.properties.get('collidable', False):
                for x, y, gid in layer:
                    tile = background_tmx.get_tile_image_by_gid(gid)
                    if tile:
                        bounding_rect = tile.get_bounding_rect()
                        tile_rect = pygame.Rect(
                            x * tile_size + bounding_rect.x * scale_factor,
                            y * tile_size + bounding_rect.y * scale_factor,
                            bounding_rect.width * scale_factor,
                            bounding_rect.height * scale_factor
                        )
                        if rect.colliderect(tile_rect):
                            return True
        return False

    def update_animation(self):
        if self.moving:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.image_index = (self.image_index + 1) % len(self.current_animation)
                self.frame_counter = 0
        else:
            self.image_index = 0
        self.image = self.current_animation[self.image_index]

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if debug:
            self.draw_debug(surface)

    def draw_debug(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.hitbox, 1)
        pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)

    def add_to_inventory(self, item):
        self.inventory[item] = self.inventory.get(item, 0) + 1
        print(f"Added {item} to inventory")
        print(f"Current inventory: {self.inventory}")

    def draw_inventory(self, surface):
        font = pygame.font.Font(None, 24)
        y_offset = 10
        for item, count in self.inventory.items():
            if count > 0:
                text = font.render(f"{item}: {count}", True, (255, 255, 255))
                surface.blit(text, (10, y_offset))
                y_offset += 20

    def draw_currency(self, surface):
        font = pygame.font.Font(None, 24)
        currency_text = font.render(f"Currency: {self.currency}", True, (255, 255, 255))
        surface.blit(currency_text, (SCREEN_WIDTH - currency_text.get_width() - 10, 10))

    def sell_crop(self, crop_type, quantity):
        if self.inventory.get(crop_type, 0) >= quantity > 0:
            self.inventory[crop_type] -= quantity
            self.currency += crop_prices.get(crop_type, 0) * quantity
            self.add_message(f"Sold {quantity} {crop_type}(s) for {crop_prices.get(crop_type, 0) * quantity} currency")

    def plant_crop(self, crop_type, x, y):
        seed_type = f"{crop_type} Seed"
        if self.inventory.get(seed_type, 0) > 0:
            self.inventory[seed_type] -= 1
            self.add_message(f"Planted {crop_type}")
            return Crop(x, y, crop_type)
        else:
            self.add_message(f"No {seed_type} available to plant.")
            return None

    def buy_item(self, item, cost):
        if self.currency >= cost:
            self.currency -= cost
            self.add_to_inventory(item)
            self.add_message(f"Bought {item} for {cost} currency")
            pygame.time.wait(200)
        else:
            self.add_message(f"Not enough currency to buy {item}.")

    def add_message(self, message):
        self.messages.append({'text': message, 'time': time.time()})

    def draw_messages(self, surface):
        current_time = time.time()
        self.messages = [msg for msg in self.messages if current_time - msg['time'] < 2]

        font = pygame.font.Font(None, 36)
        for i, message in enumerate(self.messages):
            text = font.render(message['text'], True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            surface.blit(text, text_rect)

    def sell_crops_in_market(self, market_field):
        if self.hitbox.colliderect(market_field.rect):
            for crop_type, quantity in self.inventory.items():
                if crop_type in crop_prices and quantity > 0:
                    self.sell_crop(crop_type, quantity)


class Field:
    def __init__(self, x, y, image_path):
        base_path = os.path.dirname(__file__)
        self.image = pygame.image.load(os.path.join(base_path, image_path)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))


def create_initial_field(grid_size=32):
    return [Field(10 * grid_size, 5 * grid_size, 'field/field.png')]


class Crop:
    def __init__(self, x, y, crop_type):
        self.image = None  # funktioniert vielleicht nicht
        self.crop_type = crop_type
        self.growth_stage = 0
        self.growth_timer = 0
        self.rect = pygame.Rect(x, y, 32, 32)
        self.set_image()

    growth_rates = {
        'Wheat': 30,
        'Corn': 40,
        'Tomato': 50
    }

    max_growth = 5

    def set_image(self):
        if self.growth_stage < len(crop_images[self.crop_type]):
            self.image = crop_images[self.crop_type][self.growth_stage]

    def grow(self):
        if self.growth_stage < self.max_growth:
            self.growth_timer += 1
            if self.growth_timer >= self.growth_rates[self.crop_type]:
                self.growth_stage += 1
                self.growth_timer = 0
                self.set_image()

    def interact(self, character):
        if self.growth_stage == self.max_growth and self.rect.colliderect(character.hitbox):
            character.add_to_inventory(self.crop_type)
            self.growth_stage = 0
            self.set_image()

    def check_player_position(self, character):
        if self.rect.colliderect(character.hitbox):
            self.interact(character)


def create_crops():
    return []


class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.options = ["Resume", "Save", "Load", "Quit"]
        self.selected = 0

    def draw(self, screen):
        screen.blit(popup_background, (popup_x, popup_y))
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(
                center=(SCREEN_WIDTH // 2, popup_y + popup_background.get_height() // 2 + i * 40 - 20))
            screen.blit(text, text_rect)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected = (self.selected - 1) % len(self.options)
            pygame.time.wait(200)
        if keys[pygame.K_DOWN]:
            self.selected = (self.selected + 1) % len(self.options)
            pygame.time.wait(200)
        if keys[pygame.K_RETURN]:
            return self.options[self.selected]
        return None


class CropSelector:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.crops = ["Wheat", "Corn", "Tomato"]
        self.selected = 0
        self.active = False
        self.target_field = None

    def draw(self, screen, character):
        if self.active:
            screen.blit(popup_background, (popup_x, popup_y))
            for i, crop in enumerate(self.crops):
                seed_count = character.inventory.get(f"{crop} Seed", 0)
                color = (255, 0, 0) if i == self.selected else (255, 255, 255)
                text = self.font.render(f"{crop} ({seed_count})", True, color)
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH // 2, popup_y + popup_background.get_height() // 2 + i * 40 - 40))
                screen.blit(text, text_rect)

    def handle_keys(self, crops, character):
        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.selected = (self.selected - 1) % len(self.crops)
                pygame.time.wait(200)
            if keys[pygame.K_DOWN]:
                self.selected = (self.selected + 1) % len(self.crops)
                pygame.time.wait(200)
            if keys[pygame.K_RETURN]:
                if self.target_field:

                    crops[:] = [crop for crop in crops if crop.rect.topleft != self.target_field.rect.topleft]

                    new_crop = character.plant_crop(self.crops[self.selected],
                                                    self.target_field.rect.x, self.target_field.rect.y)
                    if new_crop:
                        crops.append(new_crop)
                self.active = False
            if keys[pygame.K_ESCAPE]:
                self.active = False


class MarketField:
    def __init__(self, x, y):
        if debug:
            self.image = pygame.Surface((64, 64))
            self.image.fill((0, 0, 255))
        else:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)

        self.rect = self.image.get_rect(topleft=(x, y))
        base_path = os.path.dirname(__file__)
        self.above_image = pygame.image.load(os.path.join(base_path, "other UI", "SELL.png")).convert_alpha()
        self.above_image = pygame.transform.scale(self.above_image, (64, 32))
        self.above_rect = self.above_image.get_rect(midbottom=self.rect.midtop)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        surface.blit(self.above_image, self.above_rect.topleft)


def create_market_field(grid_size=32):
    return MarketField(10 * grid_size, 1 * grid_size)


class Shop:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.items = list(shop_items.keys())
        self.selected = 0
        self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(popup_background, (popup_x, popup_y))
            for i, item in enumerate(self.items):
                color = (255, 0, 0) if i == self.selected else (255, 255, 255)
                text = self.font.render(f"{item} ({shop_items[item]})", True, color)
                text_rect = text.get_rect(
                    center=(SCREEN_WIDTH // 2, popup_y + popup_background.get_height() // 2 + i * 40 - 40))
                screen.blit(text, text_rect)

    def handle_keys(self, character):
        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.selected = (self.selected - 1) % len(self.items)
                pygame.time.wait(200)
            if keys[pygame.K_DOWN]:
                self.selected = (self.selected + 1) % len(self.items)
                pygame.time.wait(200)
            if keys[pygame.K_RETURN]:
                item = self.items[self.selected]
                character.buy_item(item, shop_items[item])
            if keys[pygame.K_ESCAPE]:
                self.active = False


restricted_areas = [
    pygame.Rect(9 * GRID_SIZE, 0 * GRID_SIZE, 9 * GRID_SIZE, 4 * GRID_SIZE),
    pygame.Rect(6 * GRID_SIZE, 1 * GRID_SIZE, 3 * GRID_SIZE, 3 * GRID_SIZE),
    pygame.Rect(0 * GRID_SIZE, 0 * GRID_SIZE, 1 * GRID_SIZE, 20 * GRID_SIZE),
    pygame.Rect(24 * GRID_SIZE, 0 * GRID_SIZE, 1 * GRID_SIZE, 20 * GRID_SIZE),
    pygame.Rect(0 * GRID_SIZE, 19 * GRID_SIZE, 25 * GRID_SIZE, 1 * GRID_SIZE),
    pygame.Rect(0 * GRID_SIZE, 0 * GRID_SIZE, 25 * GRID_SIZE, 1 * GRID_SIZE)
]


def add_field(fields, mouse_x, mouse_y, character, field_cost):
    grid_x = (mouse_x // GRID_SIZE) * GRID_SIZE
    grid_y = (mouse_y // GRID_SIZE) * GRID_SIZE
    base_path = os.path.dirname(__file__)
    new_field = Field(grid_x, grid_y, os.path.join(base_path, "field/field.png"))

    if any(new_field.rect.colliderect(area) for area in restricted_areas):
        print("Cannot place field here.")
        return

    if all(not new_field.rect.colliderect(field.rect) for field in fields):
        if character.currency >= field_cost:
            fields.append(new_field)
            character.currency -= field_cost
            field_placed = True
            print(f"Field placed at {grid_x}, {grid_y}. Current currency: {character.currency}")
            return field_placed

        else:
            print("Not enough currency to place field.")


def draw_debug_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (255, 255, 255), (0, y), (SCREEN_WIDTH, y))


def draw_restricted_areas(surface):
    for area in restricted_areas:
        pygame.draw.rect(surface, (255, 0, 0), area, 2)


def save_game(character, fields, crops, field_cost):
    game_state = {
        'character': {
            'x': character.rect.x,
            'y': character.rect.y,
            'currency': character.currency,
            'inventory': character.inventory
        },
        'fields': [{'x': field.rect.x, 'y': field.rect.y} for field in fields],
        'crops': [{
            'x': crop.rect.x,
            'y': crop.rect.y,
            'crop_type': crop.crop_type,
            'growth_stage': crop.growth_stage,
            'growth_timer': crop.growth_timer
        } for crop in crops],
        'field_cost': field_cost  # Save the current field cost
    }
    filename = os.path.join(base_path, 'savegame.json')
    with open(filename, 'w') as file:
        json.dump(game_state, file)
    print("Game saved successfully.")


def load_game():
    filename = os.path.join(base_path, 'savegame.json')
    try:
        with open(filename, 'r') as file:
            game_state = json.load(file)
        print("Game loaded successfully.")
        return game_state
    except FileNotFoundError:
        print("No save file found.")
        return None


def main():
    character = Character(11 * GRID_SIZE + GRID_SIZE // 2, 6 * GRID_SIZE + GRID_SIZE // 2)
    fields = create_initial_field()
    crops = create_crops()
    menu = Menu()
    crop_selector = CropSelector()
    market_field = create_market_field()
    shop = Shop()
    in_menu = False
    building_mode = False

    base_path = os.path.dirname(__file__)
    field_preview_image = pygame.image.load(os.path.join(base_path, "field", "preview_field.png")).convert_alpha()
    field_preview_image = pygame.transform.scale(field_preview_image, (32, 32))

    initial_field_cost = 50
    field_cost = initial_field_cost

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if building_mode:
                    field_placed = add_field(fields, mouse_x, mouse_y, character, field_cost)
                    if field_placed:
                        field_cost = int(field_cost * 1.5)
                    else:
                        field_cost = field_cost
                else:
                    for field in fields:
                        if field.rect.collidepoint(mouse_x, mouse_y):
                            crop_selector.target_field = field
                            crop_selector.active = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if crop_selector.active:
                crop_selector.active = False
                pygame.time.wait(200)
            elif shop.active:
                shop.active = False
                pygame.time.wait(200)
            elif not (crop_selector.active or shop.active or in_menu):
                in_menu = True
        if keys[pygame.K_b] and not crop_selector.active and not shop.active and not in_menu:
            shop.active = True
        if keys[pygame.K_e] and not crop_selector.active and not shop.active and not in_menu:
            building_mode = not building_mode
            pygame.time.wait(200)

        if in_menu:
            selected_option = menu.handle_keys()
            if selected_option == "Resume":
                in_menu = False
            elif selected_option == "Save":
                save_game(character, fields, crops, field_cost)  # Save the current state including field cost
                in_menu = False
            elif selected_option == "Load":
                game_state = load_game()
                if game_state:
                    character.rect.x = game_state['character']['x']
                    character.rect.y = game_state['character']['y']
                    character.currency = game_state['character']['currency']
                    character.inventory = game_state['character']['inventory']
                    fields = [Field(field['x'], field['y'], 'field/field.png') for field in game_state['fields']]
                    crops = [Crop(crop['x'], crop['y'], crop['crop_type']) for crop in game_state['crops']]
                    for crop, state in zip(crops, game_state['crops']):
                        crop.growth_stage = 0
                        crop.growth_timer = state['growth_timer']
                    field_cost = game_state.get('field_cost', initial_field_cost)  # Load the saved field cost

                in_menu = False
            elif selected_option == "Quit":
                pygame.quit()
                sys.exit()
            menu.draw(screen)

        if not in_menu:
            screen.fill((0, 0, 0))
            draw_map()
            character.handle_keys()
            character.update_animation()

            for field in fields:
                screen.blit(field.image, field.rect.topleft)
            for crop in crops:
                crop.grow()
                crop.check_player_position(character)
                screen.blit(crop.image, crop.rect.topleft)

            market_field.draw(screen)
            character.sell_crops_in_market(market_field)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            if building_mode:
                grid_x = (mouse_x // 32) * 32
                grid_y = (mouse_y // 32) * 32
                screen.blit(field_preview_image, (grid_x, grid_y))
                font = pygame.font.Font(None, 24)
                price_text = font.render(f"Field Cost: {field_cost}", True, (255, 255, 255))
                screen.blit(price_text,
                            (SCREEN_WIDTH - price_text.get_width() - 10, SCREEN_HEIGHT - price_text.get_height() - 10))

            character.draw(screen)
            character.draw_inventory(screen)
            character.draw_currency(screen)
            character.draw_messages(screen)

            crop_selector.draw(screen, character)
            shop.draw(screen)
            crop_selector.handle_keys(crops, character)
            shop.handle_keys(character)

            if debug:
                draw_debug_grid(screen)
                draw_restricted_areas(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    main()
