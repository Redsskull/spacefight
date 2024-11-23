import pygame


# Display settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# I find I have to define enemies first for the procdeural generation to work
ENEMY_STATS = {
    "health": 50,
    "speed": 150,
    "strength": 5,
    "color": (255, 165, 0),  # Orange
    "attack_range_color": (255, 165, 0, 128),
    "stun_duration": 0.5,
    "attack_cooldown": 1.0,
    "death_blink_speed": 0.07,
    "death_duration": 0.5,
    "death_blink_duration": 0.05,
    "death_total_time": 0.5,
    "max_blinks": 15,
}

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
        "attack": {"name": "emily_kick", "frames": 5},
        "hurt": {"name": "emily_hurt", "frames": 2},
    },
    "Bart": {
        "idle": {"name": "bart_idle", "frames": 4},
        "walk": {"name": "bart_walk", "frames": 4},
        "attack": {"name": "bart_punch", "frames": 3},
        "hurt": {"name": "bart_hurt", "frames": 4},
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

# Combat settings
ATTACK_SETTINGS = {
    "cooldown": 0.1,
    "range_size": (50, 100),
    "range_color": (144, 238, 144),  # Light green
}

# Enemy attack settings
ENEMY_ATTACK = {
    "range_distance": 60,
    "range_size": (50, 100),
    "range_color": (255, 165, 0, 128),  # Semi-transparent orange
    "cooldown": 1.0,
}

# Special attack settings
SPECIAL_ATTACK_SETTINGS = {
    "cooldown": 3.0,
    "projectile": {"speed": 400, "damage": 10, "size": (20, 10)},
}

# Animation settings in config.py
ANIMATION_SETTINGS = {
    "frame_duration": 0.1,
    "special_attack_duration": 0.3,
    "death": {"blink_duration": 0.2, "total_time": 2.0, "max_blinks": 10},
}

# Enemy spawn settings
ENEMY_SPAWN = {
    "max_enemies": 10,
    "spawn_cooldown": 3.0,
    "spawn_points": [
        (-50, 447),
        (-50, 500),
        (-50, 575),
        (1250, 447),
        (1250, 500),
        (1250, 575),
    ],
}

# Level boundaries
LEVEL_BOUNDS = {"floor_y": 447, "ceiling_y": 575, "left_x": 187, "right_x": 1058}

# Character boundaries
CHARACTER_BOUNDARIES = {
    "default": {"floor_y": 400, "ceiling_y": 100, "left_x": 0, "right_x": 1000},
    "Regar": {"floor_y": 548, "ceiling_y": 354, "left_x": 80, "right_x": 1039},
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
    },
}

# UI settings
UI_SETTINGS = {
    "health_bar_width": 50,
    "health_bar_height": 5,
    "text_color": (255, 255, 255),
    "selected_color": (0, 255, 0),
    "error_color": (255, 0, 0),
}

# Player conrols
CONTROLS = {
    "player1": {
        "movement": {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
        },
        "combat": {
            "attack": 1,  # Left mouse click
            "special": 3,  # Right mouse click
        },
    },
    "player2": {
        "movement": {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
        },
        "combat": {
            "attack": pygame.K_SPACE,
            "special": pygame.K_RETURN,
        },
    },
}
