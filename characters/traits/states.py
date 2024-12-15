from enum import Enum, auto


class MovementState(Enum):
    """Character movement states"""

    IDLE = auto()
    WALKING = auto()
    RUNNING = auto()
    JUMPING = auto()
    FALLING = auto()
    ATTACKING = auto()
    STUNNED = auto()
    DEAD = auto()


class MovementStateMixin:
    """Handles movement state tracking"""

    def __init__(self):
        self.movement_state = MovementState.IDLE
        self.previous_state = MovementState.IDLE
        self.state_timer = 0

    def set_movement_state(self, state: MovementState) -> None:
        """Change movement state with history tracking"""
        self.previous_state = self.movement_state
        self.movement_state = state
        self.state_timer = 0

    def update_movement_state(self, dt: float) -> None:
        """Update movement state timing"""
        self.state_timer += dt
