import pytest
import pygame
from game import Game
from graphics import Animator, VisualEffects
from managers.animation_manager import AnimationManager
from characters.traits.animations import AnimationMixin
from characters.player_chars import Regar, Emily
from config.graphics import ANIMATION_SETTINGS
from config.characters import (
    CHARACTER_SPRITES,
    REGAR_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
)


@pytest.fixture
def animation_manager():
    """Provide initialized animation manager"""
    pygame.init()
    return AnimationManager()


def test_animation_mixin_initialization():
    """Test AnimationMixin properly initializes"""
    pygame.init()
    game = Game(1280, 720)
    char = Regar(game)  # Regar implements AnimationMixin

    # Test initialization
    assert hasattr(char, "entity_id")
    assert char.entity_id is not None
    assert not char.using_sprites
    assert not char.sprites_loaded
    assert not char.is_dying
    assert not char.is_hurt


def test_sprite_config_loading():
    """Test sprite configuration loading"""
    pygame.init()
    game = Game(1280, 720)

    # Test Regar's config
    regar = Regar(game)
    regar_config = regar._get_sprite_config()
    assert regar_config == REGAR_SPRITE_CONFIG

    # Test Emily's config
    emily = Emily(game)
    emily_config = emily._get_sprite_config()
    assert emily_config == EMILY_SPRITE_CONFIG


def test_animation_manager_registration(animation_manager):
    """Test entity registration with AnimationManager"""
    entity_id = 1
    sprite_config = REGAR_SPRITE_CONFIG

    animation_manager.register_entity(entity_id, sprite_config)

    # Verify registration
    assert entity_id in animation_manager.animators
    assert entity_id in animation_manager.effects
    assert entity_id in animation_manager.entity_configs


def test_sprite_sheet_loading(animation_manager):
    """Test sprite sheet loading through AnimationManager"""
    entity_id = 1
    name = "Regar"
    sprite_path = "assets/sprites/regar"

    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(entity_id, name, sprite_path)

    assert success
    assert entity_id in animation_manager.sprite_sheets

    sprite_sheets = animation_manager.sprite_sheets[entity_id]
    expected_animations = [
        "walk",
        "shoot",
        "attack",
    ]  # Update to match actual animations
    for anim_type in expected_animations:
        assert anim_type in sprite_sheets
        assert "surface" in sprite_sheets[anim_type]
        assert "frames" in sprite_sheets[anim_type]


def test_animation_state_transitions(animation_manager):
    """Test animation state transitions"""
    entity_id = 1
    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)

    # Test setting animations
    animation_manager.set_animation(entity_id, "idle")
    animator = animation_manager.animators[entity_id]
    assert animator.current_animation == "idle"

    animation_manager.set_animation(entity_id, "walk")
    assert animator.current_animation == "walk"


def test_visual_effects_integration(animation_manager):
    """Test visual effects integration"""
    entity_id = 1
    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)

    # Test death effect
    animation_manager.set_dying(entity_id, True)
    effects = animation_manager.effects[entity_id]
    assert effects.is_dying

    # Test hurt effect
    animation_manager.set_hurt(entity_id, True)
    assert effects.is_hurt


def test_sprite_dimensions(animation_manager):
    """Test sprite dimension calculations"""
    entity_id = 1
    name = "Regar"
    sprite_path = "assets/sprites/regar"

    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)
    animation_manager.load_sprite_sheets(entity_id, name, sprite_path)

    dimensions = animation_manager.get_sprite_dimensions(entity_id)
    assert dimensions is not None
    assert len(dimensions) == 2
    width, height = dimensions
    assert width > 0
    assert height > 0


def test_animation_update_cycle(animation_manager):
    """Test full animation update cycle"""
    entity_id = 1
    name = "Regar"
    sprite_path = "assets/sprites/regar"

    # Setup
    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)
    animation_manager.load_sprite_sheets(entity_id, name, sprite_path)

    # Use one of the known animations from the test_sprite_sheet_loading
    animation_manager.set_animation(entity_id, "walk")  # Changed from "idle" to "walk"

    # Test update
    frame = animation_manager.update_animation(entity_id, 0.016, False)
    assert frame is not None
    assert isinstance(frame, pygame.Surface)


@pytest.mark.parametrize("character_class", [Regar, Emily])
def test_character_animation_integration(character_class):
    """Test animation integration with different characters"""
    pygame.init()
    game = Game(1280, 720)
    character = character_class(game)

    # Test sprite loading
    character.load_sprite_sheets()
    assert character.sprites_loaded

    # Test animation state changes
    current_anim = character.get_current_animation()
    assert current_anim in ["idle", "walk", "attack"]
