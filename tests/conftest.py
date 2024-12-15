import pytest
import pygame
from game import Game


@pytest.fixture
def game():
    """Provide a game instance for tests"""
    pygame.init()
    game = Game(1280, 720)
    return game


@pytest.fixture
def combat_system(game):
    """Provide initialized combat system"""
    from combat.attack import Attack
    from combat.damage import DamageSystem

    damage_system = DamageSystem()
    return damage_system
