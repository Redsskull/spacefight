# Standard library
import logging
import traceback
from typing import List, Optional, Tuple, Dict, Any

# Third-party
import pygame

# Local packages
from screens.base import Screen  # Import Screen directly
from screens import (
    MainMenu,
    CharacterSelector,
    StoryScreen,
    LevelScreen,
    PauseScreen,
    GameOverScreen
)

from managers import (
    SoundManager,
    CharacterManager,
    ScreenEffectsManager,
    EnemyManager
)
from characters import Character
from game_states import GameState

logging.basicConfig(level=logging.DEBUG)


class Game:
    """
    Main game class that handles the game loop, screen changes, and initialization.
    """

    def __init__(self, screen_width, screen_height):
        """
        Initialize the game.

        Args:
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        try:
            pygame.init()
            pygame.mixer.init()
            self.SCREEN_WIDTH = screen_width
            self.SCREEN_HEIGHT = screen_height
            self.screen = pygame.display.set_mode(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )
            pygame.display.set_caption("SpaceFight")
            self.clock = pygame.time.Clock()
            self.running = True
            self.current_screen = None
            self.state = GameState.MAIN_MENU

            # initialize the game managers:
            self.sound_manager = SoundManager()
            self.character_manager = CharacterManager(self)
            self.selected_characters = []
            self.character_manager = CharacterManager(self)
            self.enemy_manager = EnemyManager(self)
            self.screen_effects = ScreenEffectsManager(
                self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
            )

            logging.info("Game initialized successfully.")

        except pygame.error as e:
            logging.error(f"Pygame error during initialization: {e}")
            print(e)
            self.running = False
        except Exception as e:
            logging.error(f"An unexpected error occurred during initialization: {e}")
            print(e)
            traceback.print_exc()
            self.running = False

    def set_selected_characters(self, selected_characters: List[Character]) -> None:
        """
        Set the selected characters for the game.

        Args:
            selected_characters (list): The list of selected characters.
        """
        self.selected_characters = selected_characters
        for i, character in enumerate(self.selected_characters):
            character.set_player_number(i + 1)

    def get_selected_characters(self):
        """
        Get the selected characters for the game.

        Returns:
            list: The list of selected characters.
        """
        return self.selected_characters

    def start(self):
        """
        Start the game by setting the current screen to MainMenu and run the game loop.
        """
        self.current_screen = MainMenu(self)
        self.run()

    def run(self):
        """
        The main game loop that handles events, update, and draw the screen.
        """
        try:
            while self.running:
                dt = self.clock.tick(60) / 1000.0  # convert to seconds
                self.handle_events()
                self.update(dt)
                self.draw()
                pygame.display.flip()
            logging.info("Game loop exited gracefully.")
        except Exception as e:
            logging.error(f"An unexpected error occurred during the game loop: {e}")
            print(e)
            traceback.print_exc()
        finally:
            pygame.quit()

    def handle_events(self):
        """
        Handle game events, including quitting.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.state == GameState.LEVEL:
                    self.change_screen(PauseScreen(self, self.current_screen))
        
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self, dt):
        """
        Update the current screen.
        Args:
            dt (float): Time since last update
        """
        if self.current_screen:
            self.current_screen.update(dt)

    def draw(self):
        """
        Draw the current screen if it exists.
        """
        if self.current_screen:
            self.current_screen.draw()

    def change_screen(self, new_screen: Screen) -> None:
        """
        Change the current screen to the new screen.
        Args:
            new_screen (Screen): The new screen to change to.
        """
        self.current_screen = new_screen
        if isinstance(new_screen, MainMenu):
            self.state = GameState.MAIN_MENU
        elif isinstance(new_screen, CharacterSelector):
            self.state = GameState.CHARACTER_SELECT
        elif isinstance(new_screen, StoryScreen):
            self.state = GameState.STORY
        elif isinstance(new_screen, LevelScreen):
            self.state = GameState.LEVEL
        elif isinstance(new_screen, PauseScreen):
            self.state = GameState.PAUSE

    def is_in_state(self, state: GameState) -> bool:
        """
        Check if the game is in a certain state.

        Args:
            state (GameState): The state to check.

        Returns:
            bool: True if the game is in the state, False otherwise.
        """
        return self.state == state

    def trigger_game_over(self):
        """Trigger game over state from any screen"""
        from screens.game_over import GameOverScreen

        self.sound_manager.stop_music()
        self.change_screen(GameOverScreen(self))
        self.state = GameState.GAME_OVER

    def reset_game(self):
        """Reset the entire game state to initial conditions"""
        # Reset game state
        self.state = GameState.MAIN_MENU
        self.current_screen = None
        self.selected_characters = []

        # Reinitialize all managers
        self.sound_manager = SoundManager()
        self.character_manager = CharacterManager(self)
        self.enemy_manager = EnemyManager(self)
        self.screen_effects = ScreenEffectsManager(
            self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        )

        # Create new main menu
        self.change_screen(MainMenu(self))