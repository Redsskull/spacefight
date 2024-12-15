"""
Will handle all basic moement from here
"""

from .boundaries import BoundaryMixin
from .states import MovementStateMixin, MovementState
import pygame
from config.controls import CONTROLS


class MovementMixin(BoundaryMixin, MovementStateMixin):
    """Handles character movement and state"""

    def __init__(self):
        BoundaryMixin.__init__(self)
        MovementStateMixin.__init__(self)
        self.direction = pygame.math.Vector2(0, 0)
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

    def move(self, dt: float) -> None:
        """Move character based on input"""
        if self.player_number is None:
            return

        keys = pygame.key.get_pressed()
        player_controls = CONTROLS[f"player{self.player_number}"]["movement"]

        # Get directional input from configured keys
        self.direction.x = (
            keys[player_controls["right"]] - keys[player_controls["left"]]
        )
        self.direction.y = keys[player_controls["down"]] - keys[player_controls["up"]]

        # Update facing direction (unless overridden by child class)
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            self.set_movement_state(MovementState.WALKING)
        else:
            self.set_movement_state(MovementState.IDLE)

        movement = self.direction * self.speed * dt
        proposed_pos = self.position + movement
        _, new_pos = self.check_boundaries(proposed_pos)
        self.position = new_pos
        self.rect.topleft = int(self.position.x), int(self.position.y)

        # Update state timing
        self.update_movement_state(dt)
