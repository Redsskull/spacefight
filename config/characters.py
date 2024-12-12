"""Character-specific configuration settings"""

import pygame

# Character stats
CHARACTER_STATS = {
    "Regar": {
        "health": 120,
        "speed": 200,
        "strength": 10,
        "color": (0, 0, 255),  # Blue
    },
    "Susan": {
        "health": 100,
        "speed": 250,
        "strength": 8,
        "color": (0, 255, 0),  # Green
    },
    "Emily": {
        "health": 90,
        "speed": 300,
        "strength": 7,
        "color": (255, 255, 0),  # Yellow
    },
    "Bart": {
        "health": 150,
        "speed": 180,
        "strength": 12,
        "color": (255, 0, 255),  # Magenta
    },
    "Enemy": ENEMY_STATS,
}

# Character sprites
CHARACTER_SPRITES = {
    "Regar": {
        "walk": {"name": "regar_walk", "frames": 6},
        "shoot": {"name": "regar_shoot", "frames": 3},
        "attack": {"name": "regar_punch", "frames": 4},
    },
    "Susan": {
        "idle": {"name": "susan_idle", "frames": 4},
        "walk": {"name": "susan_walk", "frames": 8},
        "attack": {"name": "susan_attack", "frames": 8},
        "hurt": {"name": "susan_hurt", "frames": 1},
    },
    "Emily": {
        "idle": {"name": "emily_idle", "frames": 4},
        "walk": {"name": "emily_walk", "frames": 10},
        "attack": {"name": "emily_punch", "frames": 3},
        "hurt": {"name": "emily_hurt", "frames": 2},
        "kick": {"name": "emily_kick", "frames": 5},
    },
    "Bart": {
        "idle": {"name": "bart_idle", "frames": 4},
        "walk": {"name": "bart_walk", "frames": 4},
        "attack": {"name": "bart_punch", "frames": 3},
    },
}

# Sprite settings
SPRITE_SETTINGS = {
    "TARGET_HEIGHT": 100,
    "TARGET_FRAME_WIDTH": 75,
    "DEBUG_MODE": True,  # Set to True
}

# Regar-specific sprite settings
REGAR_SPRITE_CONFIG = {
    "scale_factor": 1.5,  # Adjust if Regar appears too big/small
    "collision_offset": {
        "x": 15,  # Padding from sides of sprite
        "y": 10,  # Padding from top/bottom of sprite
    },
    "frame_widths": {
        "walk": 75,  # 600px / 6 frames
        "shoot": 75,  # 300px / 3 frames
        "attack": 75,  # 400px / 4 frames
    },
}

# Susan-specific sprite settings
SUSAN_SPRITE_CONFIG = {
    "scale_factor": 2.4,  # Keep this as we like the visual size
    "target_height": 100,  # Match SPRITE_SETTINGS["TARGET_HEIGHT"]
    "collision_offset": {
        "x": 120,  # Adjust collision box width
        "y": 60,  # Adjust collision box height
    },
    "frame_widths": {
        "idle": 128,  # 512/4 frames
        "walk": 128,  # 1024/8 frames
        "attack": 128,  # 1024/8 frames
        "hurt": 128,  # 128/1 frame
    },
}

# Emily-specific sprite settings
EMILY_SPRITE_CONFIG = {
    "scale_factor": 1.5,  # Reduced from 2.0 to make her smaller
    "target_height": 100,  # Match SPRITE_SETTINGS["TARGET_HEIGHT"]
    "collision_offset": {
        "x": 83,  # Reduced from 100 to allow more movement
        "y": 16,  # Reduced from 50 for better proportions
    },
    "frame_widths": {
        "idle": 96,  # 384/4 frames
        "walk": 96,  # 960/10 frames
        "attack": 96,  # 288/3 frames
        "hurt": 96,  # 192/2 frames
        "kick": 96,  # 480/5 frames
    },
}

# Bart-specific sprite settings
BART_SPRITE_CONFIG = {
    "scale_factor": 1.2,  # Keep this value as it gives good width
    "target_height": 100,  # Keep consistent with others
    "collision_offset": {
        "x": 70,  # Increased to reduce width (228 - 160 = 68px width)
        "y": 10,  # Reduced to make box taller (150 - 20 = 130px height)
    },
    "frame_widths": {
        "idle": 96,  # 384px / 4 frames
        "walk": 96,  # 384px / 4 frames
        "attack": 96,  # 288px / 3 frames
    },
}
