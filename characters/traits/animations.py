"""
handles all sprite and amimation related properties and methods
"""

from typing import Literal
import pygame
from config.graphics import ANIMATION_SETTINGS
from graphics import Animator, VisualEffects


class AnimationMixin:
    """Handles character animations and sprites"""

    def __init__(self):
        # Animation components
        self.animator = Animator()
        self.effects = VisualEffects()
        self.sprite_sheets = {}

        # State flags
        self.using_sprites = False
        self.sprites_loaded = False

        # Death/Hurt state management moved to VisualEffects
        self.is_dying = False
        self.is_hurt = False

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
