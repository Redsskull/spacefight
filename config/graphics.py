"""Graphics and animation configuration settings"""

# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Sprite settings
SPRITE_SETTINGS = {
    "TARGET_HEIGHT": 100,
    "TARGET_FRAME_WIDTH": 75,
    "DEBUG_MODE": True,
}

# Animation settings
ANIMATION_SETTINGS = {
    "frame_duration": 0.1,
    "special_attack_duration": 0.5,
    "death": {"blink_duration": 0.2, "total_time": 2.0, "max_blinks": 10},
}


# Level boundaries
LEVEL_BOUNDS = {"floor_y": 447, "ceiling_y": 575, "left_x": 187, "right_x": 1058}

# Character boundaries
CHARACTER_BOUNDARIES = {
    "default": {"floor_y": 400, "ceiling_y": 100, "left_x": 0, "right_x": 1000},
    "Regar": {"floor_y": 548, "ceiling_y": 354, "left_x": 80, "right_x": 1039},
    "Susan": {
        "floor_y": 548,
        "ceiling_y": 354,
        "left_x": 80,
        "right_x": 1039,
    },
    "Emily": {
        "floor_y": 548,
        "ceiling_y": 354,
        "left_x": 80,
        "right_x": 1039,
    },
    "Bart": {"floor_y": 570, "ceiling_y": 400, "left_x": 80, "right_x": 1100},
}


# Sound settings
SOUND_SETTINGS = {"default_music_volume": 0.5, "default_sound_volume": 0.5}

SOUND_REGISTRY = {
    "music": {
        "main_menu": "main_menu.mp3",
        "character_select": "Choose_your_character.mp3",
        "battle": "battlegamenoises.mp3",
        "story": "storysound.mp3",
    },
    "effects": {
        "punch": "punch.mp3",
        "metal": "metal_sound.mp3",
        "alarm": "alarm.wav",
        "shoot": "laser.mp3",
        "kick": "kick.mp3",
    },
}
