"""
Will handle all basic moement from here
"""

from .boundaries import BoundaryMixin
from .states import MovementStateMixin, MovementState
import pygame
from config.controls import CONTROLS
from config.characters import CHARACTER_STATS


class MovementMixin(BoundaryMixin, MovementStateMixin):
    """Handles character movement and input processing"""

    def __init__(self):
        BoundaryMixin.__init__(self)
        MovementStateMixin.__init__(self)
        self.direction = pygame.math.Vector2()
        self.facing_right = True
        self.base_facing_left = False
        self.position = pygame.math.Vector2()
        self.player_number = None

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

    def handle_input(self, keys: list, dt: float) -> None:
        """Handle movement input"""
        if not hasattr(self, "player_number"):
            return

        controls = CONTROLS[f"player{self.player_number}"]["movement"]

        # Get directional input
        self.direction.x = keys[controls["right"]] - keys[controls["left"]]
        self.direction.y = keys[controls["down"]] - keys[controls["up"]]

        # Update facing direction based on movement
        if self.direction.x != 0:
            self.facing_right = self.direction.x > 0

        # Normalize diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def move(self, dt: float) -> None:
        """Move character based on input"""
        if not hasattr(self, "player_number"):
            return

        # Get speed from character stats
        movement_speed = CHARACTER_STATS[self.name]["speed"]

        # Calculate movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            # Use proper speed from stats
            movement = self.direction * movement_speed * dt
            self.position += movement
            self.rect.topleft = (int(self.position.x), int(self.position.y))
            self.set_movement_state(MovementState.WALKING)
        else:
            self.set_movement_state(MovementState.IDLE)
