import pytest
import pygame
from game import Game
from graphics import SpriteLoader, Animator, VisualEffects
from config import (
    CHARACTER_SPRITES,
    ANIMATION_SETTINGS,
    REGAR_SPRITE_CONFIG,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SPRITE_SETTINGS,
)


def test_sprite_loader():
    """Test sprite loading and scaling"""
    pygame.init()
    # Initialize display using config settings
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Test loading Regar's sprites - use same path as characters.py
    sprite_path = "assets/sprites/regar"
    sprite_sheets = SpriteLoader.load_character_sprites("Regar")

    # Verify correct animations are loaded
    for anim_type, info in CHARACTER_SPRITES["Regar"].items():
        assert anim_type in sprite_sheets
        sprite_name = info["name"]
        full_path = f"{sprite_path}/{sprite_name}.png"

        # Verify sprite properties match config
        sheet = sprite_sheets[anim_type]
        assert "surface" in sheet
        assert "frames" in sheet
        assert sheet["frames"] == info["frames"]

        # Verify scaling using SPRITE_SETTINGS for target height
        surface = sheet["surface"]
        expected_height = int(
            SPRITE_SETTINGS["TARGET_HEIGHT"] * REGAR_SPRITE_CONFIG["scale_factor"]
        )
        assert surface.get_height() == expected_height

    # Clean up display
    pygame.display.quit()


def test_animator():
    """Test animation state management"""
    pygame.init()
    animator = Animator()

    # Test initial state
    assert animator.current_animation is None
    assert animator.animation_frame == 0
    assert animator.animation_timer == 0

    try:
        # Test animation update with mock sprite sheets if real ones unavailable
        mock_sprite_sheets = {
            "walk": {"surface": pygame.Surface((100, 100)), "frames": 4}
        }
        animator.current_animation = "walk"
        frame = animator.update(0.016, mock_sprite_sheets, False)
        assert frame is not None

        # Test frame progression
        animator.animation_timer = ANIMATION_SETTINGS["frame_duration"]
        frame = animator.update(0.016, mock_sprite_sheets, False)
        assert animator.animation_frame == 1
    except pygame.error:
        pytest.skip("Animation test skipped due to sprite loading error")


def test_visual_effects():
    """Test death and hurt effects"""
    pygame.init()
    effects = VisualEffects()

    # Test death effect
    assert not effects.is_dying
    effects.is_dying = True
    sprite = pygame.Surface((50, 50))

    # Test blink effect - let enough time pass for a blink
    effects.update_death_effect(effects.death_blink_duration + 0.001, sprite)
    assert effects.blink_count > 0

    # Test hurt effect
    assert not effects.is_hurt
    effects.is_hurt = True
    effects.update_hurt_effect(0.016)
    assert effects.hurt_timer < effects.hurt_duration
