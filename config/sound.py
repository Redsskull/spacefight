"""Sound-related configuration settings"""

# Sound settings
SOUND_SETTINGS = {"default_music_volume": 0.5, "default_sound_volume": 0.5}

# Sound registry mapping IDs to filenames
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

__all__ = ["SOUND_SETTINGS", "SOUND_REGISTRY"]
