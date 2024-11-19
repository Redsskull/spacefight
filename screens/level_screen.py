import pygame
from .base import Screen
from config import LEVEL_BOUNDS, CHARACTER_BOUNDARIES


class LevelScreen(Screen):
    """
    This is the level one screen where the characters will battle enemies
    Args:
        Screen (Screen): Base class for all screens
    """

    def __init__(self, game):
        """
        Initialize the level one screen
        Args:
            game (Game): The game instance
        """
        super().__init__(game)
        self.game = game
        self.initialize_assets()
        self.initialize_sounds()
        self.initialize_characters()

        # Define boundries

        self.floor_y = LEVEL_BOUNDS["floor_y"]
        self.ceiling_y = LEVEL_BOUNDS["ceiling_y"]
        self.left_x =  LEVEL_BOUNDS["left_x"]
        self.right_x = LEVEL_BOUNDS["right_x"]

    def initialize_assets(self):
        """
        Initialize the assets for the level one screen
        """
        self.background = pygame.image.load("assets/art/level_one.webp").convert()
        self.background = pygame.transform.scale(
            self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )

    def initialize_sounds(self):
        """
        Initialize the sounds for the level one screen
        """
        self.game.sound_manager.stop_music()
        self.game.sound_manager.play_music("battle")

    def initialize_characters(self):
        """
        Initialize the players for the level one screen
        """
        selected_characters = self.game.get_selected_characters()
        self.game.character_manager.initialize_characters_for_level(selected_characters)

    def update(self, dt):
        """
        Update the level one screen
        Args:
            dt (float): Time since last update
        """
        dt = self.game.clock.get_time() / 1000  # Convert to seconds
        self.game.character_manager.update_characters(dt)
        self.game.enemy_manager.update(dt)
        self.limit_character_movement()

        # First check if any characters are still alive
        all_dead = all(
            char.health <= 0 for char in self.game.character_manager.active_characters
        )

        # Then check if all dead characters have finished their animations this is especially important if there is a player 2
        if all_dead:
            animations_complete = all(
                char.animation_complete
                for char in self.game.character_manager.active_characters
            )
            if animations_complete:
                self.game.trigger_game_over()

    def limit_character_movement(self):
        """Limit the characters movement to their boundaries"""
        for character in self.game.character_manager.active_characters:
            boundaries = CHARACTER_BOUNDARIES.get(
                character.name, 
                CHARACTER_BOUNDARIES["default"]
            )
            
            # Vertical movement
            if character.position.y < boundaries["ceiling_y"]:
                character.position.y = boundaries["ceiling_y"]
                character.rect.y = int(boundaries["ceiling_y"])
            elif character.position.y > boundaries["floor_y"]:
                character.position.y = boundaries["floor_y"]
                character.rect.y = int(boundaries["floor_y"])
                
            # Horizontal movement
            if character.position.x < boundaries["left_x"]:
                character.position.x = boundaries["left_x"]
                character.rect.x = int(boundaries["left_x"])
            elif character.position.x > boundaries["right_x"]:
                character.position.x = boundaries["right_x"]
                character.rect.x = int(boundaries["right_x"])

    def draw(self):
        """
        Draw the level one screen
        """
        self.screen.blit(self.background, (0, 0))
        self.game.character_manager.draw_characters(self.screen)
        self.game.enemy_manager.draw(self.screen)
        self.game.character_manager.draw_ui(self.screen)

    # def handle_events(self, events):
    #     """
    #     Handle events for the level one screen
    #     Args:
    #         events (Event): The events to handle
    #     """
    #     # Handle any level-specific events here
    #     # (like character movement, attacks, etc)
    #     self.game.character_manager.handle_events(events)

    # I don't appear to need a handle_events method here.


