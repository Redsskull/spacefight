import pygame
from typing import Optional
import config


class MovementMixin:
    """Handles character movement logic and controls"""

    def __init__(self):
        self.direction = pygame.math.Vector2()
        self.facing_right = True
        self.base_facing_left = False  # Can be overridden by specific characters

    def move(self, dt: float) -> None:
        """Handle movement based on input"""
        if not hasattr(self, "player_number") or self.player_number is None:
            return

        keys = pygame.key.get_pressed()
        controls = config.CONTROLS[f"player{self.player_number}"]["movement"]

        # Get directional input
        self.direction.x = keys[controls["right"]] - keys[controls["left"]]
        self.direction.y = keys[controls["down"]] - keys[controls["up"]]

        # Update facing direction
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        # Apply movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            self.position += self.direction * self.speed * dt

        # Update rect position
        self.rect.topleft = (int(self.position.x), int(self.position.y))
