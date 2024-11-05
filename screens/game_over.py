import pygame
from .base import Screen
from screens.main_menu import MainMenu


class GameOverScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("GAME OVER", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(
            center=(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2)
        )
        self.start_time = pygame.time.get_ticks()
        self.display_duration = 5000  # 5 seconds

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.display_duration:
            self.game.change_screen(MainMenu(self.game))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)
