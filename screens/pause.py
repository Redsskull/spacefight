import pygame
from pygame.constants import (
    KEYDOWN,
    K_ESCAPE,
)  # this is a new way I read aoout keydown in pygame. if it workss TODO: use it in the whole game
from game_states import GameState
from managers.enemy_manager import EnemyManager
from .base import Screen


class PauseScreen(Screen):
    """Pause screen that overlays the game
    Args:
        screen (pygame.Surface): The screen surface
    """

    def __init__(self, game):
        """Initialize the pause screen"""
        super().__init__(game)
        self.previous_state = None
        # Rest of initialization code...

        # UI Constants
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
        self.BUTTON_PADDING = 20
        self.font = pygame.font.Font(None, 36)

        # Menu items
        self.menu_items = ["Resume", "Options", "Main Menu", "Exit Game"]
        self.selected_index = 0

        # Create button rectangles and text
        self.buttons = []
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255, 255, 255))
            rect = pygame.Rect(
                self.game.SCREEN_WIDTH // 2 - self.BUTTON_WIDTH // 2,
                self.game.SCREEN_HEIGHT // 2
                - 100
                + i * (self.BUTTON_HEIGHT + self.BUTTON_PADDING),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
            )
            self.buttons.append((text, rect))

    def on_enter(self, **kwargs):
        """Initialize when entering screen"""
        super().on_enter()
        # Get previous_state from kwargs if provided
        self.previous_state = kwargs.get("previous_state", GameState.MAIN_MENU)
        # Pause logic - could stop animations, enemy AI, etc.

    def on_exit(self):
        """Clean up when exiting screen"""
        # Resume logic - restart animations, enemy AI, etc.
        super().on_exit()

    def handle_events(self, events):
        """
        Handle events for the pause screen.
        Args:
            events (List[Event]): A list of pygame events
        """
        for event in events:
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(
                        self.menu_items
                    )
                elif event.key == pygame.K_RETURN:
                    self.select_menu_item()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    for i, (_, rect) in enumerate(self.buttons):
                        if rect.collidepoint(mouse_pos):
                            self.selected_index = i
                            self.select_menu_item()

    def select_menu_item(self):
        """Handle menu selection"""
        if self.menu_items[self.selected_index] == "Resume":
            self.game.screen_manager.change_screen(self.previous_state)
        # Rest of menu handling...
        elif self.menu_items[self.selected_index] == "Options":
            print("Options menu - Coming soon!")
        elif self.menu_items[self.selected_index] == "Main Menu":
            # Reset entire game state by reinitializing MainMenu
            self.game.sound_manager.stop_music()
            self.game.reset_game()
            from .main_menu import MainMenu

            self.game.change_screen(MainMenu(self.game))
        elif self.menu_items[self.selected_index] == "Exit Game":
            self.game.running = False

    def draw(self):
        """
        Draw the pause screen.
        """
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))

        # Draw "PAUSED" text
        pause_text = self.font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 100))
        self.screen.blit(pause_text, pause_rect)

        # Draw buttons
        for i, (text, rect) in enumerate(self.buttons):
            # Highlight selected button
            color = (100, 100, 255) if i == self.selected_index else (50, 50, 50)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            # Center text in button
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
