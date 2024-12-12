"""Test suite for enemy system"""

import pytest
import pygame
from game import Game
from enemies import BaseEnemy, BasicEnemy
from characters.player_chars import Character, Regar  # Import Regar for testing


def test_enemy_initialization():
    """Test basic enemy initialization"""
    pygame.init()
    game = Game(1280, 720)
    spawn_pos = (100, 100)
    enemy = BasicEnemy(game, spawn_pos)

    # Test initial state
    assert enemy.state.value == "spawning"
    assert enemy.base_facing_left is True
    assert enemy.facing_right is False
    assert enemy.position == pygame.math.Vector2(spawn_pos)


def test_enemy_facing_direction():
    """Test enemy facing direction updates based on target"""
    pygame.init()
    game = Game(1280, 720)
    enemy = BasicEnemy(game, (100, 100))

    # Create mock target using Regar as he's a standard character
    target = Regar(game)
    target.position = pygame.math.Vector2(50, 100)  # Set initial position
    enemy.target = target
    enemy.update_facing()
    assert not enemy.facing_right

    # Test facing right
    target.position = pygame.math.Vector2(150, 100)
    enemy.target = target
    enemy.update_facing()
    assert enemy.facing_right


def test_enemy_sprite_config():
    """Test enemy sprite configuration"""
    pygame.init()
    game = Game(1280, 720)
    enemy = BasicEnemy(game, (100, 100))

    # Test sprite configuration loaded
    assert hasattr(enemy, "sprite_config")
    assert hasattr(enemy, "sprite_data")
    assert enemy.sprite_config["scale_factor"] == 1.0
    assert "idle" in enemy.sprite_data
    assert "walk" in enemy.sprite_data
    assert "attack" in enemy.sprite_data
