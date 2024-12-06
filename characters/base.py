from typing import Optional
import pygame
import config


class BaseCharacter(pygame.sprite.Sprite):
    """Base class for all characters with core attributes"""

    def __init__(self, name: str, game: "Game") -> None:
        super().__init__()
        # Core identity
        self.name = name
        self.game = game
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
        self.position = pygame.math.Vector2()
        self.visible = True

    def set_player_number(self, number: int) -> None:
        """Set the player number for controls"""
        self.player_number = number
