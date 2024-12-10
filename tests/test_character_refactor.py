import pygame
import pytest
from game import Game
from characters.player_chars import Regar, Susan, Emily, Bart
from combat.projectiles import EnergyShot
import config
from enemy import Enemy


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

        # Animation trait - only test for attributes, not loaded sprites
        assert hasattr(char, "using_sprites")
        assert hasattr(char, "sprite_sheets")
        assert hasattr(char, "animator")
        assert hasattr(char, "effects")

    # Test specific character attributes
    assert regar.ranged_attacker is True
    assert regar.has_special_attack is True
    assert susan.has_special_attack is False
    assert emily.has_special_attack is True
    assert bart.base_facing_left is True


def test_movement_mixin(monkeypatch):
    """Test movement matches original functionality"""
    pygame.init()
    game = Game(1280, 720)
    char = Regar(game)

    # Test initial position setting
    char.set_position(100, 100)
    char.set_player_number(1)

    # Mock pygame.key.get_pressed() to simulate held right key
    keys = [0] * 323  # Create a list of key states
    keys[config.CONTROLS["player1"]["movement"]["right"]] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)

    # Test movement
    char.move(0.016)
    assert char.position.x > 100
    assert char.rect.topleft == (int(char.position.x), int(char.position.y))


def test_regar_special_attack_trigger(monkeypatch):
    """Test Regar's energy shot special attack"""
    pygame.init()
    game = Game(1280, 720)
    regar = Regar(game)
    regar.set_player_number(1)

    # Mock right mouse button press (index 2) for player 1 special attack
    mouse_buttons = [0, 0, 1]  # [left, middle, right]
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: mouse_buttons)

    # Test initial state
    assert not regar.is_special_attacking
    assert len(regar.projectiles) == 0

    # Trigger special attack
    regar.attack(0.016)  # Process input

    # Verify projectile creation
    assert regar.is_special_attacking
    assert len(regar.projectiles) == 1


def test_emily_special_attack_trigger(monkeypatch):
    """Test Emily's kick special attack"""
    pygame.init()
    game = Game(1280, 720)
    emily = Emily(game)
    emily.set_player_number(1)

    # Setup test enemy
    enemy = Enemy(game, (emily.rect.x + 100, emily.rect.y))
    game.enemy_manager.enemies.add(enemy)
    initial_enemy_health = enemy.health

    # Mock right mouse button press for player 1 special attack
    mouse_buttons = [0, 0, 1]  # [left, middle, right]
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda: mouse_buttons)

    # Test initial state
    assert not emily.is_special_attacking

    # Trigger special attack
    emily.attack(0.016)

    # Verify kick execution and damage
    assert emily.is_special_attacking
    assert enemy.health < initial_enemy_health


def test_susan_combat():
    """Test Susan's combat mechanics"""
    pygame.init()
    game = Game(1280, 720)
    susan = Susan(game)

    # Verify Susan has no special attack
    assert not susan.has_special_attack
    assert not hasattr(susan, "perform_special_attack")

    # Test normal attack is working
    assert susan.attack_timer <= 0
    susan.start_attack()
    assert susan.attacking
    assert susan.attack_timer > 0


def test_bart_facing(monkeypatch):
    """Test Bart's unique facing direction"""
    pygame.init()
    game = Game(1280, 720)
    bart = Bart(game)

    # Test initial attributes
    assert bart.base_facing_left  # Sprites face left by default
    assert bart.facing_right  # Should start facing right like others

    bart.set_player_number(1)

    # Test moving right
    keys = [0] * 323
    keys[config.CONTROLS["player1"]["movement"]["right"]] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)
    bart.move(0.016)
    assert bart.facing_right

    # Test moving left
    keys = [0] * 323
    keys[config.CONTROLS["player1"]["movement"]["left"]] = 1
    monkeypatch.setattr(pygame.key, "get_pressed", lambda: keys)
    bart.move(0.016)
    assert not bart.facing_right
