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
        self.all_characters = [Regar(), Susan(), Emily(), Bart()]
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
        self.character_group.draw(screen)

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

    def handle_character_movement(self, dt):
        """
        Handle character movement.
        Args:
            dt (float): Time since last update
        """
        keys = pygame.key.get_pressed()
        for character in self.active_characters:
            character.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
            character.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
            character.move(dt)

    def handle_character_attack(self):
        """
        Handle character attacks.
        """
        mouse = pygame.mouse.get_pressed()
        if mouse[0] or mouse[2]:  # Left or right mouse button
            for character in self.active_characters:
                character.attack()

    # TODO: Add player2 conrols
    # TODO: add controller support

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

