import pytest
import pygame
from game import Game
from characters.player_chars import Regar
from characters.traits.boundaries import BoundaryMixin
from characters.traits.states import MovementState, MovementStateMixin
from characters.traits.movement import MovementMixin


def test_boundary_mixin():
    """Test boundary checking functionality"""
    pygame.init()

    # Test basic boundary setup
    boundary = BoundaryMixin()
    assert boundary.bounds["left"] == 0
    assert boundary.bounds["right"] == 1280

    # Test boundary setting
    boundary.set_boundaries(10, 1270, 10, 710)
    assert boundary.bounds["left"] == 10
    assert boundary.bounds["top"] == 10

    # Test position correction
    outside_pos = pygame.math.Vector2(-10, 800)
    is_outside, corrected = boundary.check_boundaries(outside_pos)
    assert is_outside
    assert corrected.x == 10  # Should be corrected to left boundary
    assert corrected.y == 710  # Should be corrected to bottom boundary


def test_movement_state_tracking():
    """Test movement state management"""
    pygame.init()
    state_mixin = MovementStateMixin()

    # Test initial state
    assert state_mixin.movement_state == MovementState.IDLE
    assert state_mixin.previous_state == MovementState.IDLE
    assert state_mixin.state_timer == 0

    # Test state transition
    state_mixin.set_movement_state(MovementState.WALKING)
    assert state_mixin.movement_state == MovementState.WALKING
    assert state_mixin.previous_state == MovementState.IDLE

    # Test state timing
    state_mixin.update_movement_state(0.016)
    assert state_mixin.state_timer == 0.016


def test_integrated_movement():
    """Test integrated movement with boundaries and states"""
    pygame.init()
    game = Game(1280, 720)
    char = Regar(game)
    char.set_player_number(1)

    # Test movement within bounds
    char.set_position(100, 100)
    char.move(0.016)  # Just pass dt
    assert char.movement_state == MovementState.IDLE  # No keys pressed

    # Test boundary collision
    char.set_position(-50, -50)
    char.move(0.016)  # Remove direction vector
    assert char.position.x >= 0
    assert char.position.y >= 0

    # Test state transition to idle
    char.move(0.016)  # Remove direction vector
    assert char.movement_state == MovementState.IDLE


@pytest.mark.parametrize(
    "direction",
    [
        pygame.math.Vector2(1, 0),  # Right
        pygame.math.Vector2(-1, 0),  # Left
        pygame.math.Vector2(0, 1),  # Down
        pygame.math.Vector2(0, -1),  # Up
    ],
)
def test_boundary_directions(direction):
    """Test boundary checking in all directions"""
    boundary = BoundaryMixin()

    # Position at edge based on direction
    pos = pygame.math.Vector2(
        1280 if direction.x > 0 else 0 if direction.x < 0 else 640,
        720 if direction.y > 0 else 0 if direction.y < 0 else 360,
    )

    # Move slightly outside bounds
    test_pos = pos + direction * 50
    is_outside, corrected = boundary.check_boundaries(test_pos)

    assert is_outside
    assert corrected != test_pos
