import pytest
import pygame
from game import Game
from game_states import GameState
from screens.main_menu import MainMenu
from screens.story_screen import StoryScreen
from screens.character_selector import CharacterSelector
from screens.level_screen import LevelScreen
from screens.pause import PauseScreen
from screens.game_over import GameOverScreen
from characters.player_chars import Regar  # Import Regar for testing


@pytest.fixture
def game():
    """Initialize pygame and game instance"""
    pygame.init()
    return Game(1280, 720)


@pytest.fixture
def game_with_level(game):
    """Setup game with a level and character"""
    # Create and select Regar first
    regar = Regar(game)
    game.set_selected_characters([regar])

    # Then change to level screen
    game.screen_manager.change_screen(GameState.LEVEL)
    return game


def test_screen_manager_initialization(game):
    """Test screen manager initializes correctly"""
    assert game.screen_manager is not None
    assert game.screen_manager.current_screen is not None
    assert isinstance(game.screen_manager.current_screen, MainMenu)
    assert game.state == GameState.MAIN_MENU


def test_screen_registration(game):
    """Test screen registration"""
    # These should be registered in Game.__init__
    assert GameState.MAIN_MENU in game.screen_manager.registered_screens
    assert GameState.CHARACTER_SELECT in game.screen_manager.registered_screens
    assert GameState.STORY in game.screen_manager.registered_screens
    assert GameState.LEVEL in game.screen_manager.registered_screens
    assert GameState.PAUSE in game.screen_manager.registered_screens
    assert GameState.GAME_OVER in game.screen_manager.registered_screens


def test_screen_transitions(game):
    """Test screen transitions"""
    # Test initial state
    assert isinstance(game.screen_manager.current_screen, MainMenu)

    # Test transition to story
    game.screen_manager.change_screen(GameState.STORY)
    assert isinstance(game.screen_manager.current_screen, StoryScreen)
    assert game.state == GameState.STORY
    assert isinstance(game.screen_manager.previous_screen, MainMenu)

    # Test transition to character select
    game.screen_manager.change_screen(GameState.CHARACTER_SELECT)
    assert isinstance(game.screen_manager.current_screen, CharacterSelector)
    assert game.state == GameState.CHARACTER_SELECT


def test_invalid_screen_transition(game, caplog):
    """Test handling of invalid screen transitions"""
    initial_screen = game.screen_manager.current_screen

    # Try to transition to non-existent state
    game.screen_manager.change_screen("INVALID_STATE")

    # Screen shouldn't change
    assert game.screen_manager.current_screen == initial_screen
    # Should log an error
    assert any(
        "No screen registered for state" in record.message for record in caplog.records
    )


def test_screen_lifecycle(game):
    """Test screen lifecycle hooks"""
    # Change to story screen which should trigger initialization
    game.screen_manager.change_screen(GameState.STORY)
    story_screen = game.screen_manager.current_screen
    assert isinstance(story_screen, StoryScreen)

    # Change to another screen to test exit
    game.screen_manager.change_screen(GameState.CHARACTER_SELECT)
    assert game.screen_manager.previous_screen == story_screen
    assert isinstance(game.screen_manager.current_screen, CharacterSelector)


def test_pause_screen_handling(game):
    """Test pause screen specific behavior"""
    # Setup character first
    regar = Regar(game)
    game.set_selected_characters([regar])

    # Start with level screen
    game.screen_manager.change_screen(GameState.LEVEL)
    level_screen = game.screen_manager.current_screen
    assert isinstance(level_screen, LevelScreen)

    # Test pause/resume cycle
    game.screen_manager.change_screen(GameState.PAUSE)
    assert isinstance(game.screen_manager.current_screen, PauseScreen)
    assert game.state == GameState.PAUSE

    # Resume should return to level screen
    game.screen_manager.change_screen(GameState.LEVEL)
    assert isinstance(game.screen_manager.current_screen, LevelScreen)
    assert game.state == GameState.LEVEL


def test_pause_resume_state(game_with_level):
    """Test pause/resume maintains correct state"""
    # Get initial game state
    initial_state = game_with_level.state
    assert isinstance(game_with_level.screen_manager.current_screen, LevelScreen)

    # Pause game with previous_state in kwargs
    game_with_level.screen_manager.change_screen(
        GameState.PAUSE, previous_state=initial_state
    )
    assert game_with_level.state == GameState.PAUSE

    # Resume game - should return to level
    pause_screen = game_with_level.screen_manager.current_screen
    assert isinstance(pause_screen, PauseScreen)
    assert pause_screen.previous_state == initial_state


def test_character_preservation_during_pause(game_with_level):
    """Test that characters are preserved during pause/resume cycle"""
    # Get initial character state
    initial_characters = game_with_level.character_manager.active_characters
    assert len(initial_characters) > 0  # Should have Regar from fixture

    # Store character positions
    initial_positions = [
        (char.name, char.position.copy()) for char in initial_characters
    ]

    # Pause game
    game_with_level.screen_manager.change_screen(
        GameState.PAUSE, previous_state=GameState.LEVEL
    )
    assert game_with_level.state == GameState.PAUSE

    # Resume game
    game_with_level.screen_manager.change_screen(GameState.LEVEL)

    # Verify characters preserved
    resumed_characters = game_with_level.character_manager.active_characters
    assert len(resumed_characters) == len(initial_characters)

    # Verify character states maintained
    for char in resumed_characters:
        initial_pos = next(pos for name, pos in initial_positions if name == char.name)
        assert char.position == initial_pos


def test_character_clear_with_preserve(game_with_level):
    """Test character clear with preservation"""
    initial_characters = game_with_level.character_manager.active_characters
    assert len(initial_characters) > 0

    # Clear with preservation
    game_with_level.character_manager.clear(preserve_selected=True)

    # Verify selected characters preserved
    preserved_characters = game_with_level.character_manager.active_characters
    assert len(preserved_characters) == len(game_with_level.selected_characters)
    assert all(
        char in preserved_characters for char in game_with_level.selected_characters
    )


def test_character_clear_full_reset(game_with_level):
    """Test character clear with full reset"""
    assert len(game_with_level.character_manager.active_characters) > 0

    # Full clear
    game_with_level.character_manager.clear(preserve_selected=False)

    # Verify all characters cleared
    assert len(game_with_level.character_manager.active_characters) == 0
    assert len(game_with_level.character_manager.character_group) == 0
