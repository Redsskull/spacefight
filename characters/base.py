"""
Will set the base character for all characters in the game
"""

import pygame
import config


class BaseCharacter(pygame.sprite.Sprite):
    """
    Base class for all characters with core attributes
    Args:
        pygame (pygame.sprite.Sprite): Base class for all sprites
    """

    def __init__(self, name: str, game: "Game") -> None:
        """
        Initialize the base character
        Args:
            name (str): The name of the character
            game (Game): The game instance
        """
        super().__init__()
        # Core identity
        self.name = name
        self.game = game
        self.direction = pygame.math.Vector2(0, 0)
        self.player_number = None

        # Load stats from config
        stats = config.CHARACTER_STATS[name]
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.speed = stats["speed"]
        self.strength = stats["strength"]
        self.color = stats["color"]

        # Basic sprite setup
        self.image = pygame.Surface((50, 100))
        self.rect = self.image.get_rect()
        self.visible = True

    def set_player_number(self, number: int) -> None:
        """Set the player number for controls
        Args:
            number (int): The player number
        """
        self.player_number = number
