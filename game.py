# Standard library
import logging
import traceback
from typing import List, Optional, Tuple, Dict, Any

# Third-party
import pygame

# Local packages
from screens.base import Screen
from screens import (
    MainMenu,
    CharacterSelector,
    StoryScreen,
    LevelScreen,
    PauseScreen,
    GameOverScreen,
)

from managers import (
    SoundManager,
    CharacterManager,
    ScreenEffectsManager,
    EnemyManager,
    AnimationManager,
    CombatManager,
    ScreenManager,
)

# Import Character from new modular structure
from characters.player_chars import Character

# Import states
from game_states import GameState

# Import configs
from config.graphics import SCREEN_WIDTH, SCREEN_HEIGHT, CHARACTER_BOUNDARIES
from config.characters import CHARACTER_STATS

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

            # Initialize managers in correct order
            self.animation_manager = AnimationManager()
            self.sound_manager = SoundManager()
            self.character_manager = CharacterManager(self)
            self.combat_manager = CombatManager(self)
            self.selected_characters = []
            self.enemy_manager = EnemyManager(self)
            self.screen_effects = ScreenEffectsManager(
                self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT
            )

            # Initialize screen manager
            self.screen_manager = ScreenManager(self)

            # Register screens
            self.screen_manager.register_screen(GameState.MAIN_MENU, MainMenu)
            self.screen_manager.register_screen(
                GameState.CHARACTER_SELECT, CharacterSelector
            )
            self.screen_manager.register_screen(GameState.STORY, StoryScreen)
            self.screen_manager.register_screen(GameState.LEVEL, LevelScreen)
            self.screen_manager.register_screen(GameState.PAUSE, PauseScreen)
            self.screen_manager.register_screen(GameState.GAME_OVER, GameOverScreen)

            # Start with main menu
            self.screen_manager.change_screen(GameState.MAIN_MENU)

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
        self.screen_manager.handle_events(events)

    def update(self, dt):
        """
        Update the current screen.
        Args:
            dt (float): Time since last update
        """
        self.screen_manager.update(dt)

    def draw(self):
        """
        Draw the current screen if it exists.
        """
        self.screen_manager.draw()

    def change_screen(self, new_state: GameState, **kwargs):
        """
        Change the current screen to the new screen.
        Args:
            new_state (GameState): The new state to change to.
        """
        self.screen_manager.change_screen(new_state, **kwargs)

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
        self.sound_manager.stop_music()
        self.screen_manager.change_screen(GameState.GAME_OVER)

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
        self.change_screen(GameState.MAIN_MENU)

    def pause_game(self):
        """Pause the game"""
        previous_state = self.state
        self.screen_manager.change_screen(
            GameState.PAUSE, previous_state=previous_state
        )
