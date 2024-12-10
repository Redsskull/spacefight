"""
Handles loading and scaling of sprite sheets
"""

import pygame
import logging
from typing import Dict
from config import (
    CHARACTER_SPRITES,
    SPRITE_SETTINGS,
    REGAR_SPRITE_CONFIG,
    SUSAN_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
    BART_SPRITE_CONFIG,
)


class SpriteLoader:
    """Handles loading and configuring sprite sheets"""

    @staticmethod
    def load_character_sprites(character_name: str) -> Dict[str, Dict]:
        """Load all sprites for a character"""
        sprite_sheets = {}
        sprite_path = f"assets/sprites/{character_name.lower()}"

        try:
            # Get character-specific config
            sprite_config = {
                "Regar": REGAR_SPRITE_CONFIG,
                "Susan": SUSAN_SPRITE_CONFIG,
                "Emily": EMILY_SPRITE_CONFIG,
                "Bart": BART_SPRITE_CONFIG,
            }.get(character_name)

            if not sprite_config:
                raise ValueError(f"No sprite config found for {character_name}")

            # Use target height from SPRITE_SETTINGS if not in character config
            target_height = sprite_config.get(
                "target_height", SPRITE_SETTINGS["TARGET_HEIGHT"]
            )

            # Load each animation type
            for anim_type, info in CHARACTER_SPRITES[character_name].items():
                sprite_name = info["name"]
                full_path = f"{sprite_path}/{sprite_name}.png"
                original_surface = pygame.image.load(full_path).convert_alpha()

                # Calculate scaling like in characters.py
                base_height_scale = target_height / original_surface.get_height()
                final_scale = base_height_scale * sprite_config["scale_factor"]
                scaled_width = int(original_surface.get_width() * final_scale)
                scaled_height = int(target_height * sprite_config["scale_factor"])

                scaled_surface = pygame.transform.scale(
                    original_surface, (scaled_width, scaled_height)
                )

                sprite_sheets[anim_type] = {
                    "surface": scaled_surface,
                    "frames": info["frames"],
                }

        except Exception as e:
            logging.error(f"Failed to load sprites for {character_name}: {e}")
            return {}

        return sprite_sheets
