"""
A manager for all character calls in the game. 
This class will be used to initialize characters and draw them, 
but characters.py will handle the movement and attacks
"""

import logging
from typing import List, Optional
import pygame
from characters import Character  # This will get the original Character class
from characters import (
    Regar,
    Susan,
    Emily,
    Bart,
)  # And the original character implementations


class CharacterManager:
    """
    Manages the characters in the game.
    I will call on this class whenever I need to update the characters, draw them, or handle their movement and attacks.
    """

    def __init__(self, game: "Game") -> None:
        """
        Initialize the CharacterManager.
        Args:
            game (Game): The game instance
        important, this is where the sorite group is created..
        """
        self.game = game
        self.all_characters: List[Character] = [
            Regar(game),
            Susan(game),
            Emily(game),
            Bart(game),
        ]
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
                    logging.error("Invalid character at index %d", i)
                    continue

                x = 75 + i * (station_width + 25)
                y = 300
                character.rect.topleft = (x, y)
                character.position = pygame.math.Vector2(x, y)

            self.character_group.empty()
            self.character_group.add(self.active_characters)

        except AttributeError as e:
            logging.error("Character initialization failed: %s", e)
            raise

    def initialize_characters_for_level(self, selected_characters):
        """Initialize the characters for the level screen."""
        try:
            if not selected_characters:
                raise ValueError("No characters selected")

            self.active_characters = selected_characters
            screen_height = getattr(self.game, "SCREEN_HEIGHT", 720)

            for i, character in enumerate(self.active_characters):
                if not character:
                    logging.warning("Skipping invalid character at index %d", i)
                    continue

                # Position character
                x = 100 + (i * 100)
                y = screen_height - 150
                character.rect.midbottom = (x, y)
                character.position = pygame.math.Vector2(
                    x, y - character.rect.height // 2
                )

                # Load sprite sheets for level
                character.load_sprite_sheets()

            self.character_group.empty()
            self.character_group.add([c for c in self.active_characters if c])

        except Exception as e:
            logging.error("Failed to initialize characters: %s", e)
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

                x_position = padding + (character.player_number - 1) * (
                    bar_width + padding
                )

                # Draw player number
                font = pygame.font.Font(None, 36)
                player_text = f"P{character.player_number}"
                text_surface = font.render(player_text, True, (255, 255, 255))
                screen.blit(text_surface, (x_position, y_position))

                # Draw health bar background
                health_bar_bg = pygame.Rect(
                    x_position, y_position + 30, bar_width, bar_height
                )
                pygame.draw.rect(screen, (255, 0, 0), health_bar_bg)

                # Draw current health
                if character.health > 0:
                    current_health_width = (
                        character.health / character.max_health
                    ) * bar_width
                    current_health_bar = pygame.Rect(
                        x_position, y_position + 30, current_health_width, bar_height
                    )
                    pygame.draw.rect(screen, (0, 255, 0), current_health_bar)

                # Draw health text
                health_text = f"{character.health}/{character.max_health}"
                text_surface = font.render(health_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(
                    center=(
                        x_position + bar_width / 2,
                        y_position + 30 + bar_height / 2,
                    )
                )
                screen.blit(text_surface, text_rect)

            except (AttributeError, TypeError) as e:
                logging.warning("Failed to draw UI for character: %s", e)
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
