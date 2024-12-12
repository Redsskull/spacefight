"""Enemy-specific configuration settings"""

import pygame

# Base enemy stats
BASE_ENEMY_STATS = {
    "health": 50,
    "speed": 150,
    "strength": 5,
    "color": (255, 165, 0),  # Orange
    "stun_duration": 0.5,
    "death_blink_speed": 0.07,
    "death_duration": 0.5,
    "death_blink_duration": 0.05,
    "death_total_time": 0.5,
    "max_blinks": 15,
}

ENEMY_STATS = BASE_ENEMY_STATS  # Alias for compatibility

__all__ = ["BASE_ENEMY_STATS", "ENEMY_STATS"]

# Enemy types - for future expansion
ENEMY_TYPES = {
    "basic": {
        **BASE_ENEMY_STATS,
    },
    "fast": {
        **BASE_ENEMY_STATS,
        "health": 30,
        "speed": 250,
        "strength": 3,
        "color": (255, 100, 100),
    },
    "tank": {
        **BASE_ENEMY_STATS,
        "health": 100,
        "speed": 100,
        "strength": 8,
        "color": (165, 42, 42),
    },
}

# Enemy sprite configuration
ENEMY_SPRITE_CONFIG = {
    "scale_factor": 1.0,
    "target_height": 100,
    "collision_offset": {
        "x": 20,
        "y": 10,
    },
    "frame_widths": {
        "idle": 96,
        "walk": 96,
        "attack": 96,
    },
}

# Enemy animation frames
ENEMY_SPRITES = {
    "basic": {
        "idle": {"name": "enemy_idle", "frames": 4},
        "walk": {"name": "enemy_walk", "frames": 6},
        "attack": {"name": "enemy_attack", "frames": 5},
        "hurt": {"name": "enemy_hurt", "frames": 3},
    }
}
