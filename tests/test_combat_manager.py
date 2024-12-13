"""Test suite for combat manager"""

import pytest
import pygame
from game import Game
from managers.combat_manager import CombatManager
from characters.player_chars import Regar, Emily
from enemies import BasicEnemy
from combat.attack import Attack
from combat.projectiles import EnergyShot


@pytest.fixture
def combat_manager():
    """Provide initialized combat manager"""
    pygame.init()
    game = Game(1280, 720)
    return game.combat_manager


def test_combat_manager_initialization(combat_manager):
    """Test combat manager initializes correctly"""
    assert combat_manager.damage_system is not None
    assert combat_manager.projectile_system is not None
    assert isinstance(combat_manager.active_attacks, dict)
    assert isinstance(combat_manager.attack_collisions, list)


def test_melee_collision_detection(combat_manager):
    """Test melee attack collision detection"""
    # Setup character and enemy
    char = Regar(combat_manager.game)
    enemy = BasicEnemy(combat_manager.game, (100, 100))

    # Add to respective managers
    combat_manager.game.character_manager.active_characters.append(char)
    combat_manager.game.enemy_manager.enemies.add(enemy)

    # Position character next to enemy
    char.position = pygame.math.Vector2(150, 100)
    char.rect.center = char.position
    char.attacking = True

    # Test collision detection
    combat_manager._check_melee_collisions()
    assert enemy.health < enemy.max_health


def test_projectile_collision_detection(combat_manager):
    """Test projectile collision detection"""
    # Setup
    enemy = BasicEnemy(combat_manager.game, (100, 100))
    combat_manager.game.enemy_manager.enemies.add(enemy)

    # Create projectile
    combat_manager.projectile_system.spawn_projectile(
        EnergyShot,
        (90, 100),  # Position near enemy
        pygame.math.Vector2(1, 0),
        damage=15,
        speed=500,
    )

    # Test collision
    initial_health = enemy.health
    combat_manager._check_projectile_collisions()
    assert enemy.health < initial_health


def test_attack_registration(combat_manager):
    """Test attack registration and state tracking"""
    # Create attack
    entity_id = 1
    attack = Attack("test_attack", 10, (50, 50), 0.5)

    # Register attack
    combat_manager.register_attack(entity_id, attack)
    assert entity_id in combat_manager.active_attacks

    # Test attack state updates
    combat_manager._update_attack_states(0.6)  # Update past cooldown
    assert entity_id not in combat_manager.active_attacks


def test_enemy_attack_handling(combat_manager):
    """Test enemy attack collision with player"""
    # Setup
    char = Regar(combat_manager.game)
    enemy = BasicEnemy(combat_manager.game, (100, 100))

    # Position character near enemy
    char.position = pygame.math.Vector2(150, 100)
    char.rect.center = char.position

    # Trigger enemy attack
    enemy.attacking = True
    initial_health = char.health

    # Test collision
    combat_manager.handle_enemy_attack(enemy, char)
    assert char.health < initial_health


def test_combat_manager_clear(combat_manager):
    """Test clearing combat states"""
    # Setup some state
    entity_id = 1
    attack = Attack("test_attack", 10, (50, 50), 0.5)
    combat_manager.register_attack(entity_id, attack)
    combat_manager.projectile_system.spawn_projectile(
        EnergyShot, (100, 100), pygame.math.Vector2(1, 0), damage=15, speed=500
    )

    # Test clear
    combat_manager.clear()
    assert len(combat_manager.active_attacks) == 0
    assert len(combat_manager.projectile_system.active_projectiles) == 0
    assert len(combat_manager.attack_collisions) == 0
