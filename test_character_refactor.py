import pygame
import pytest
from game import Game
from characters.player_chars import Regar, Susan, Emily, Bart


def test_character_initialization():
    """Test basic character initialization with new trait system"""
    pygame.init()
    game = Game(1280, 720)

    # Test each character
    regar = Regar(game)
    susan = Susan(game)
    emily = Emily(game)
    bart = Bart(game)

    # Test trait initialization
    for char in [regar, susan, emily, bart]:
        # Movement trait
        assert hasattr(char, "direction")
        assert hasattr(char, "facing_right")

        # Combat trait
        assert hasattr(char, "attacking")
        assert hasattr(char, "attack_timer")
        assert hasattr(char, "attack_range")

        # Animation trait
        assert hasattr(char, "using_sprites")
        assert hasattr(char, "sprite_sheets")
        assert hasattr(char, "animation_timer")

    # Test specific character attributes
    assert regar.ranged_attacker is True
    assert regar.has_special_attack is True

    assert susan.has_special_attack is False

    assert emily.has_special_attack is True

    assert bart.base_facing_left is True


def test_movement_mixin():
    """Test movement functionality"""
    pygame.init()
    game = Game(1280, 720)
    char = Regar(game)

    # Set initial position
    char.position.x = 100
    char.position.y = 100
    char.set_player_number(1)

    # Simulate movement
    char.move(0.016)  # Simulate one frame at ~60fps

    # Position should update based on movement
    assert char.rect.topleft == (int(char.position.x), int(char.position.y))
