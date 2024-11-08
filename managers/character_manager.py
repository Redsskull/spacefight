import pygame
from characters import Regar, Susan, Emily, Bart


class CharacterManager:
    """
    Manages the characters in the game.
    I will call on this class whenever I need to update the characters, draw them, or handle their movement and attacks.
    """

    def __init__(self, game):
        """
        Initialize the CharacterManager.
        Args:
            game (Game): The game instance
        important, this is where the sorite group is created..
        """
        self.game = game
        self.all_characters = [Regar(game), Susan(game), Emily(game), Bart(game)]
        self.active_characters = []
        self.character_group = pygame.sprite.Group()
        for character in self.all_characters:
            self.character_group.add(character)

    def initialize_characters_for_story(self):
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

    def initialize_characters_for_level(self, selected_characters):
        """
        Initialize the characters for the level screen.
        Args:
            selected_characters (list): The characters selected by the player
        """
        self.active_characters = selected_characters
        for i, character in enumerate(self.active_characters):
            x = 100 + (i * 100)
            y = self.game.SCREEN_HEIGHT - 150
            character.rect.midbottom = (x, y)
            character.position = pygame.math.Vector2(x, y - character.rect.height // 2)
        self.character_group.empty()
        self.character_group.add(self.active_characters)

    def draw_characters(self, screen):
        """
        Draw the characters on the screen.
        Args:
            screen (pygame.Surface): The screen surface
        """
        for character in self.active_characters:
            character.draw(screen)

    def draw_ui(self, screen):
        """Draw UI elements for player characters
        Args:
            screen (pygame.Surface): The screen surface
        """
        padding = 10
        bar_height = 20
        bar_width = 200
        y_position = padding

        for character in self.active_characters:
            if hasattr(
                character, "player_number"
            ):  # Only draw UI for player characters
                font = pygame.font.Font(None, 24)
                name_surface = font.render(
                    character.name, True, (255, 255, 0)
                )  # Bright yellow
                screen.blit(name_surface, (padding, y_position))

                # Draw health bar background (red)
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        padding + name_surface.get_width() + 5,
                        y_position,
                        bar_width,
                        bar_height,
                    ),
                )

                # Draw current health (green)
                health_percentage = character.health / character.max_health
                current_health_width = bar_width * health_percentage
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (
                        padding + name_surface.get_width() + 5,
                        y_position,
                        current_health_width,
                        bar_height,
                    ),
                )
                y_position += bar_height + padding

    def get_character_by_name(self, name):
        """
        Get a character by name.
        Args:
            name (str): The name of the character
        Returns:
            Character: The character with the given name, or None if not found
        """
        return next((char for char in self.all_characters if char.name == name), None)

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
