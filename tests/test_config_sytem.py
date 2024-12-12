import pytest
import pygame
from game import Game
from graphics import SpriteLoader, Animator, VisualEffects
from config.characters import CHARACTER_STATS, CHARACTER_SPRITES, REGAR_SPRITE_CONFIG
from config.combat import ATTACK_SETTINGS, SPECIAL_ATTACK_SETTINGS
from config.graphics import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SETTINGS,
    ANIMATION_SETTINGS,
)
from config.controls import CONTROLS


def test_character_configs():
    """Test character configuration values match original"""
    # Test character stats
    assert CHARACTER_STATS["Regar"]["health"] == 120
    assert CHARACTER_STATS["Susan"]["speed"] == 250

    # Test sprite configurations
    assert "walk" in CHARACTER_SPRITES["Regar"]
    assert REGAR_SPRITE_CONFIG["scale_factor"] == 1.5


def test_combat_configs():
    """Test combat configuration values match original"""
    assert "cooldown" in ATTACK_SETTINGS["default"]
    assert "Emily" in SPECIAL_ATTACK_SETTINGS
    assert SPECIAL_ATTACK_SETTINGS["Emily"]["damage"] == 50


def test_graphics_configs():
    """Test graphics configuration values match original"""
    assert SCREEN_WIDTH == 1280
    assert SCREEN_HEIGHT == 720
    assert "TARGET_HEIGHT" in SPRITE_SETTINGS
    assert "frame_duration" in ANIMATION_SETTINGS


def test_control_configs():
    """Test control configuration values match original"""
    assert "movement" in CONTROLS["player1"]
    assert "combat" in CONTROLS["player2"]
