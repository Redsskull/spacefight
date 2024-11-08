import pygame
from .base import Screen
from screens.main_menu import MainMenu
from game_states import GameState


class GameOverScreen(Screen):
    """
    The game over screen.
    Args:
        screen (pygame.Surface): The screen surface
    """
    def __init__(self, game):
        """
        Initialize the game over screen.
        Args:
            screen (pygame.Surface): The screen surface
        """
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
        self.display_duration = 5000  # 7 seconds
        self.subtitle_delay = 1000  # 2 second delay for subtitle

    def update(self, dt):
        """
        Update the game over screen.
        Args:
            dt (float): Time since last update
        """   
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.display_duration:
            self.game.reset_game()

    def draw(self):
        """
        Draw the game over screen.
        """
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)

        # Only show subtitle after delay
        if pygame.time.get_ticks() - self.start_time >= self.subtitle_delay:
            self.screen.blit(self.subtitle, self.subtitle_rect)
