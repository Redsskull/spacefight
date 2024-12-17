import pytest
import pygame
import os
from game import Game
from managers.animation_manager import AnimationManager
from characters.player_chars import Regar, Emily
from config.characters import (
    CHARACTER_SPRITES,
    REGAR_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
)
from config.enemies import ENEMY_SPRITES, ENEMY_SPRITE_CONFIG


@pytest.fixture
def game():
    """Initialize pygame and game instance"""
    pygame.init()
    pygame.display.set_mode((1280, 720))  # Need display mode for sprite loading
    return Game(1280, 720)


@pytest.fixture
def animation_manager():
    """Provide initialized animation manager"""
    pygame.init()
    pygame.display.set_mode((1280, 720))
    return AnimationManager()


@pytest.fixture
def regar(game):
    """Create Regar instance with loaded sprites"""
    pygame.display.init()  # Ensure display is initialized
    character = Regar(game)
    character.load_sprite_sheets()  # This should now work with display initialized
    return character


@pytest.fixture
def emily(game):
    """Create Emily instance with loaded sprites"""
    pygame.display.init()  # Ensure display is initialized
    character = Emily(game)
    character.load_sprite_sheets()  # This should now work with display initialized
    return character


@pytest.mark.parametrize(
    "character,config,animations",
    [
        ("Regar", REGAR_SPRITE_CONFIG, ["walk", "shoot", "attack"]),  # Capitalize!
        ("Emily", EMILY_SPRITE_CONFIG, ["idle", "walk", "attack", "hurt", "kick"]),
    ],
)
def test_character_animations(animation_manager, character, config, animations):
    """Test loading and validating actual character animations"""
    entity_id = 1
    sprite_path = f"assets/sprites/{character.lower()}"

    animation_manager.register_entity(entity_id, config)
    success = animation_manager.load_sprite_sheets(entity_id, character, sprite_path)

    assert success
    for anim in animations:
        assert anim in CHARACTER_SPRITES[character]  # Check in CHARACTER_SPRITES first
        assert anim in animation_manager.sprite_sheets[entity_id]


def test_regar_walk_animation(regar):
    """Test Regar's walk animation frames"""
    walk_frames = CHARACTER_SPRITES["Regar"]["walk"]["frames"]
    assert walk_frames == 6
    assert "walk" in regar.sprite_sheets
    sheet = regar.sprite_sheets["walk"]["surface"]
    frame_width = sheet.get_width() // walk_frames
    assert frame_width > 0


def test_emily_attack_animation(emily):
    """Test Emily's attack animation frames"""
    attack_frames = CHARACTER_SPRITES["Emily"]["attack"]["frames"]
    assert attack_frames == 3
    assert "attack" in emily.sprite_sheets
    sheet = emily.sprite_sheets["attack"]["surface"]
    frame_width = sheet.get_width() // attack_frames
    assert frame_width > 0


def test_animation_timing(animation_manager):
    """Test animation timing with real sprites"""
    entity_id = 1
    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(
        entity_id, "Regar", "assets/sprites/regar"
    )
    assert success

    # Set the initial animation
    animation_manager.set_animation(entity_id, "walk")

    # Now test frame progression
    walk_frames = CHARACTER_SPRITES["Regar"]["walk"]["frames"]
    for _ in range(walk_frames):
        frame = animation_manager.update_animation(entity_id, 0.1, False)
        assert frame is not None
        # Optional: Add frame dimension checks
        assert frame.get_width() > 0
        assert frame.get_height() > 0


def test_sprite_files_exist():
    """Verify sprite files exist in assets directory"""
    base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sprites")

    # Test Regar's sprites
    regar_path = os.path.join(base_path, "regar")
    assert os.path.exists(regar_path)
    for anim in CHARACTER_SPRITES["Regar"]:
        sprite_name = CHARACTER_SPRITES["Regar"][anim]["name"]
        assert os.path.exists(os.path.join(regar_path, f"{sprite_name}.png"))

    # Test Emily's sprites
    emily_path = os.path.join(base_path, "emily")
    assert os.path.exists(emily_path)
    for anim in CHARACTER_SPRITES["Emily"]:
        sprite_name = CHARACTER_SPRITES["Emily"][anim]["name"]
        assert os.path.exists(os.path.join(emily_path, f"{sprite_name}.png"))


def test_enemy_animations(animation_manager):
    """Test enemy sprite loading and animation"""
    pygame.init()
    entity_id = 1
    sprite_path = "assets/sprites/enemy"

    # Register enemy with config
    animation_manager.register_entity(entity_id, ENEMY_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(entity_id, "basic", sprite_path)

    assert success

    # Verify all animations loaded
    expected_animations = ["idle", "walk", "attack", "hurt"]
    for anim in expected_animations:
        assert anim in ENEMY_SPRITES["basic"]
        assert anim in animation_manager.sprite_sheets[entity_id]

        # Verify frame counts
        sheet = animation_manager.sprite_sheets[entity_id][anim]
        assert sheet["frames"] == ENEMY_SPRITES["basic"][anim]["frames"]

        # Verify sprite dimensions
        surface = sheet["surface"]
        frame_width = surface.get_width() // sheet["frames"]
        assert frame_width > 0
        assert surface.get_height() == int(
            ENEMY_SPRITE_CONFIG["target_height"] * ENEMY_SPRITE_CONFIG["scale_factor"]
        )


def test_enemy_sprite_files():
    """Verify enemy sprite files exist"""
    sprite_path = os.path.join("assets", "sprites", "enemy")
    assert os.path.exists(sprite_path)

    for anim_type, info in ENEMY_SPRITES["basic"].items():
        sprite_name = info["name"]
        assert os.path.exists(os.path.join(sprite_path, f"{sprite_name}.png"))


def test_character_combat_animations(animation_manager):
    """Test character animations during combat"""
    # Initialize character
    entity_id = 1
    animation_manager.register_entity(entity_id, REGAR_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(
        entity_id, "Regar", "assets/sprites/regar"
    )
    assert success

    # Test attack animation
    animation_manager.set_animation(entity_id, "attack")
    frame = animation_manager.update_animation(entity_id, 0.1, False)
    assert frame is not None
    assert frame.get_width() > 0


def test_enemy_combat_animations(animation_manager):
    """Test enemy animations during combat"""
    entity_id = 1
    animation_manager.register_entity(entity_id, ENEMY_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(
        entity_id, "basic", "assets/sprites/enemy"
    )
    assert success

    # Test transition from idle to attack
    animation_manager.set_animation(entity_id, "idle")
    idle_frame = animation_manager.update_animation(entity_id, 0.1, False)
    assert idle_frame is not None

    animation_manager.set_animation(entity_id, "attack")
    attack_frame = animation_manager.update_animation(entity_id, 0.1, False)
    assert attack_frame is not None


def test_movement_animation_sync():
    """Test animation syncs with movement"""
    pygame.init()
    game = Game(1280, 720)
    regar = Regar(game)

    # Simulate movement right
    regar.direction = pygame.math.Vector2(1, 0)
    regar.facing_right = True
    assert regar.get_current_animation() == "walk"

    # Simulate stopping - should still be walk since Regar has no idle
    regar.direction = pygame.math.Vector2(0, 0)
    assert regar.get_current_animation() == "walk"  # Not idle!

    # Test attack animation
    regar.attacking = True
    assert regar.get_current_animation() == "attack"

    # Test special attack
    regar.is_special_attacking = True
    assert regar.get_current_animation() == "shoot"


def test_special_attack_animation_sequence(animation_manager):
    """Test special attack animation completion"""
    entity_id = 1
    animation_manager.register_entity(entity_id, EMILY_SPRITE_CONFIG)
    success = animation_manager.load_sprite_sheets(
        entity_id, "Emily", "assets/sprites/emily"
    )
    assert success

    # Test kick animation sequence
    animation_manager.set_animation(entity_id, "kick")
    frames = []
    for _ in range(CHARACTER_SPRITES["Emily"]["kick"]["frames"]):
        frame = animation_manager.update_animation(entity_id, 0.1, False)
        frames.append(frame)

    # Verify all frames were generated
    assert all(frame is not None for frame in frames)
    assert len(frames) == CHARACTER_SPRITES["Emily"]["kick"]["frames"]


def test_emily_movement_animation_sync():
    """Test Emily's animation syncs with movement"""
    pygame.init()
    game = Game(1280, 720)
    emily = Emily(game)

    # Test idle state
    emily.direction = pygame.math.Vector2(0, 0)
    assert emily.get_current_animation() == "idle"

    # Test walking
    emily.direction = pygame.math.Vector2(1, 0)
    assert emily.get_current_animation() == "walk"


def test_animation_state_priority():
    """Test animation state priority order"""
    pygame.init()
    game = Game(1280, 720)

    # Test Regar's priority
    regar = Regar(game)
    regar.is_special_attacking = True
    assert (
        regar.get_current_animation() == "shoot"
    )  # Special attack should override walk

    regar.is_special_attacking = False
    regar.attacking = True
    assert regar.get_current_animation() == "attack"  # Attack should override walk

    # Test Emily's priority
    emily = Emily(game)
    emily.direction = pygame.math.Vector2(0, 0)
    assert emily.get_current_animation() == "idle"  # No movement should be idle

    emily.direction = pygame.math.Vector2(1, 0)
    assert emily.get_current_animation() == "walk"  # Movement should be walk
