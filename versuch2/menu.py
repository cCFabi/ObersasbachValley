import pygame

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 74)
        self.start_button = self.font.render('Start', True, (255, 255, 255))
        self.button_rect = self.start_button.get_rect(center=(screen_width // 2, screen_height // 2))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.start_button, self.button_rect.topleft)

    def update(self, mouse_pos, mouse_click):
        if self.button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            return True
        return False
