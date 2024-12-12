"""
Handles visual effects like death animation and hurt states
"""

import pygame
from config.graphics import ANIMATION_SETTINGS


class VisualEffects:
    """Manages visual effects for characters"""

    def __init__(self):
        # Death effect properties
        self.is_dying = False
        self.death_blink_duration = ANIMATION_SETTINGS["death"]["blink_duration"]
        self.death_total_time = ANIMATION_SETTINGS["death"]["total_time"]
        self.death_blink_timer = self.death_blink_duration
        self.blink_count = 0
        self.max_blinks = ANIMATION_SETTINGS["death"]["max_blinks"]
        self.animation_complete = False

        # Hurt effect properties
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = ANIMATION_SETTINGS["frame_duration"]

    def update_death_effect(self, dt: float, sprite: pygame.Surface) -> bool:
        """Update death animation effect"""
        if not self.is_dying:
            return False

        self.death_total_time -= dt
        self.death_blink_timer -= dt

        if self.death_blink_timer <= 0:
            self.death_blink_timer = self.death_blink_duration
            self.blink_count += 1  # Make sure this increment happens
            return True  # Return True when a blink occurs

        return False

    def update_hurt_effect(self, dt: float) -> None:
        """Update hurt state effect"""
        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False
