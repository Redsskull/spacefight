"""
Will handle all basic moement from here
"""

import pygame
from config.controls import CONTROLS


class MovementMixin:
    """Handles character movement logic and controls"""

    def __init__(self):
        self.direction = pygame.math.Vector2()
        self.base_facing_left = False
        self.facing_right = not self.base_facing_left
        self.position = pygame.math.Vector2()

    def set_base_facing(self, facing_left: bool):
        """Update base facing direction and initial facing_right value"""
        self.base_facing_left = facing_left
        self.facing_right = not facing_left

    def set_position(self, x: float, y: float) -> None:
        """Set position and update rect"""
        self.position.x = x
        self.position.y = y
        if hasattr(self, "rect"):
            self.rect.topleft = (int(x), int(y))

    def move(self, dt: float) -> None:
        """Move character based on input"""
        if self.player_number is None:
            return

        keys = pygame.key.get_pressed()
        player_controls = CONTROLS[f"player{self.player_number}"]["movement"]

        self.direction.x = (
            keys[player_controls["right"]] - keys[player_controls["left"]]
        )
        self.direction.y = keys[player_controls["down"]] - keys[player_controls["up"]]

        # Update facing direction
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        # Apply normalized movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            movement = self.direction * self.speed * dt
            self.position += movement
            self.rect.topleft = (int(self.position.x), int(self.position.y))
