from typing import Literal
import pygame
from config import CHARACTER_SPRITES, ANIMATION_SETTINGS


class AnimationMixin:
    """Handles character animations and sprites"""

    def __init__(self):
        self.using_sprites = False
        self.sprites_loaded = False
        self.sprite_sheets = {}
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = ANIMATION_SETTINGS["frame_duration"]

        # Death animation properties
        self.is_dying = False
        self.death_blink_duration = ANIMATION_SETTINGS["death"]["blink_duration"]
        self.death_total_time = ANIMATION_SETTINGS["death"]["total_time"]
        self.death_blink_timer = self.death_blink_duration
        self.blink_count = 0
        self.max_blinks = ANIMATION_SETTINGS["death"]["max_blinks"]
        self.animation_complete = False

        # Hurt properties
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = ANIMATION_SETTINGS["frame_duration"]

    def get_current_animation(
        self,
    ) -> Literal["idle", "walk", "attack", "shoot", "hurt", "kick"]:
        """Determine which animation to use based on state"""
        if self.is_hurt and "hurt" in self.sprite_sheets:
            return "hurt"
        if self.is_special_attacking:
            if self.ranged_attacker and "shoot" in self.sprite_sheets:
                return "shoot"
            elif "kick" in self.sprite_sheets:
                return "kick"
        elif self.attacking:
            return "attack"
        elif self.direction.length() > 0:
            return "walk"

        return "idle" if "idle" in self.sprite_sheets else "walk"
