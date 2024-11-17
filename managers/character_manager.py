import pygame
import logging
from typing import List, Optional, Tuple
from characters import Regar, Susan, Emily, Bart, Character 


class CharacterManager:
    """
    Manages the characters in the game.
    I will call on this class whenever I need to update the characters, draw them, or handle their movement and attacks.
    """

    def __init__(self, game: 'Game') -> None:
        """
        Initialize the CharacterManager.
        Args:
            game (Game): The game instance
        important, this is where the sorite group is created..
        """
        self.game = game
        self.all_characters: List[Character] = [Regar(game), Susan(game), Emily(game), Bart(game)]
        self.active_characters: List[Character] = []
        self.character_group: pygame.sprite.Group = pygame.sprite.Group()
        for character in self.all_characters:
            self.character_group.add(character)

    def initialize_characters_for_story(self) -> None:
        """
        Initialize the characters in the story screen.
        """
        self.active_characters = self.all_characters
        station_width = (self.game.SCREEN_WIDTH - 150) // 4
        for i, character in enumerate(self.active_characters):
            x = 75 + i * (station_width + 25)
            y = 300
            character.rect.topleft = (x, y)
            character.position = pygame.math.Vector2(x, y)
        self.character_group.empty()
        self.character_group.add(self.active_characters)

    def initialize_characters_for_selection(self) -> None:
        """Initialize characters for selection screen with error handling."""
        try:
            station_width = 150
            for i, character in enumerate(self.active_characters):
                if not character:
                    logging.error(f"Invalid character at index {i}")
                    continue
                    
                x = 75 + i * (station_width + 25)
                y = 300
                character.rect.topleft = (x, y)
                character.position = pygame.math.Vector2(x, y)
                
            self.character_group.empty()
            self.character_group.add(self.active_characters)
            
        except AttributeError as e:
            logging.error(f"Character initialization failed: {e}")
            raise

    def initialize_characters_for_level(self, selected_characters):
        """Initialize the characters for the level screen."""
        try:
            if not selected_characters:
                raise ValueError("No characters selected")
                
            self.active_characters = selected_characters
            screen_height = getattr(self.game, 'SCREEN_HEIGHT', 720)
            
            for i, character in enumerate(self.active_characters):
                if not character:
                    logging.warning(f"Skipping invalid character at index {i}")
                    continue
                    
                # Position character
                x = 100 + (i * 100)
                y = screen_height - 150
                character.rect.midbottom = (x, y)
                character.position = pygame.math.Vector2(x, y - character.rect.height // 2)
                
                # Load sprite sheets for level
                character.load_sprite_sheets()
                    
            self.character_group.empty()
            self.character_group.add([c for c in self.active_characters if c])
            
        except Exception as e:
            logging.error(f"Failed to initialize characters: {e}")
            raise

    def draw_characters(self, screen):
        """
        Draw the characters on the screen.
        Args:
            screen (pygame.Surface): The screen surface
        """
        for character in self.active_characters:
            character.draw(screen)

    def draw_ui(self, screen):
        """Draw UI elements with error handling.
        Args:
            screen (pygame.Surface): The screen surface
        """
        if not screen:
            logging.error("Invalid screen surface")
            return
            
        padding = 10
        bar_height = 20
        bar_width = 200
        y_position = padding

        for character in self.active_characters:
            try:
                if not hasattr(character, "player_number"):
                    continue
                    
                # UI drawing logic here
                
            except (AttributeError, TypeError) as e:
                logging.warning(f"Failed to draw UI for character: {e}")
                continue

    def get_character_by_name(self, name: str) -> Optional[Character]:
        """
        Get a character by name.
        Args:
            name (str): The name of the character
        Returns:
            Character: The character with the given name, or None if not found
        """
        for character in self.all_characters:
            if character.name == name:
                return character
        return None

    def update_characters(self, dt):
        """
        Update the characters in the game.
        Args:
            dt (float): Time since last update
        """
        for character in self.active_characters:
            character.update(dt)

    def get_character_info(self):
        """
        Get information about the characters.
        Returns:
            list: A list of tuples containing character information
        """
        return [
            (char.name, char.health, char.speed, char.strength)
            for char in self.all_characters
        ]