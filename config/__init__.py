"""Configuration package exposing all settings"""

from .enemies import *  # Import enemy configs first
from .characters import *
from .combat import *
from .graphics import *
from .controls import *
from .sound import *

__all__ = [
    # Enemy configs
    "ENEMY_STATS",
    "BASE_ENEMY_STATS",
    # Character configs
    "CHARACTER_STATS",
    "CHARACTER_SPRITES",
    "REGAR_SPRITE_CONFIG",
    "SUSAN_SPRITE_CONFIG",
    "EMILY_SPRITE_CONFIG",
    "BART_SPRITE_CONFIG",
    # Combat configs
    "ATTACK_SETTINGS",
    "SPECIAL_ATTACK_SETTINGS",
    # Graphics configs
    "SCREEN_WIDTH",
    "SCREEN_HEIGHT",
    "SPRITE_SETTINGS",
    "ANIMATION_SETTINGS",
    # Sound configs
    "SOUND_SETTINGS",
    "SOUND_REGISTRY",
    # Control configs
    "CONTROLS",
]
