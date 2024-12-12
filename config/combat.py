"""Combat-related configuration settings"""

import pygame

# Combat settings
ATTACK_SETTINGS = {
    "default": {
        "cooldown": 0.1,
        "range_size": (50, 100),
        "range_color": (144, 238, 144),  # Light green
    },
    "Regar": {
        "cooldown": 0.1,
        "range_size": (50, 100),
        "range_color": (144, 238, 144),
        "offset": {
            "x": 15,
            "y": 10,
        },
    },
    "Susan": {
        "cooldown": 0.1,
        "range_size": (50, 100),
        "range_color": (144, 238, 144),
        "offset": {
            "x": 120,
            "y": 60,
        },
    },
    "Emily": {
        "cooldown": 0.1,
        "range_size": (50, 100),
        "range_color": (144, 238, 144),
        "offset": {
            "x": 35,
            "y": 15,
        },
    },
    "Bart": {  # Add Bart's attack settings
        "cooldown": 0.1,
        "range_size": (50, 100),
        "range_color": (144, 238, 144),
        "offset": {
            "x": 70,  # Match his collision offset
            "y": 10,  # Match his collision offset
        },
    },
}

# Special attack settings
SPECIAL_ATTACK_SETTINGS = {
    "cooldown": 2.0,  # Global cooldown
    "Emily": {
        "damage": 50,  # High damage for kick
        "range": {"width": 120, "height": 63},  #  Matched from dimensions
        "offset": {"x": 60, "y": 0},  # Adjusted for kick animation
        "cooldown": 1.5,  # Specific cooldown for Emily
        "duration": 0.5,  # Duration of the animation
    },
}
