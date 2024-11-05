import pygame
from .base import Screen
from screens.main_menu import MainMenu
from game_states import GameState


class GameOverScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
        # Main game over text
        self.font = pygame.font.Font(None, 74)
        self.text = self.font.render("GAME OVER", True, (255, 0, 0))
        self.text_rect = self.text.get_rect(
            center=(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2)
        )

        # Subtitle text
        self.subtitle_font = pygame.font.Font(None, 36)
        self.subtitle = self.subtitle_font.render(
            "Now Bart will never get the girl...", True, (255, 0, 0)
        )
        self.subtitle_rect = self.subtitle.get_rect(
            center=(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT // 2 + 50)
        )

        self.start_time = pygame.time.get_ticks()
        self.display_duration = 5000  # 5 seconds
        self.subtitle_delay = 1000  # 1 second delay for subtitle

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.display_duration:
            self.game.reset_game()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)

        # Only show subtitle after delay
        if pygame.time.get_ticks() - self.start_time >= self.subtitle_delay:
            self.screen.blit(self.subtitle, self.subtitle_rect)
