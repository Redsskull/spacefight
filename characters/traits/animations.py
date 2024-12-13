"""
handles all sprite and amimation related properties and methods
"""

from typing import Literal
import pygame
from config.graphics import ANIMATION_SETTINGS
from graphics import Animator, VisualEffects
from config.characters import (
    REGAR_SPRITE_CONFIG,
    SUSAN_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
    BART_SPRITE_CONFIG,
)


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

        self.entity_id = id(self)  # Use object id as entity id
        self.game.animation_manager.register_entity(
            self.entity_id, self._get_sprite_config()
        )

    def _get_sprite_config(self):
        """Get sprite configuration based on character name"""
        configs = {
            "Regar": REGAR_SPRITE_CONFIG,
            "Susan": SUSAN_SPRITE_CONFIG,
            "Emily": EMILY_SPRITE_CONFIG,
            "Bart": BART_SPRITE_CONFIG,
        }
        return configs.get(self.name)

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

    def update_animation(self, dt: float):
        """Update animation state using animation manager"""
        current_anim = self.get_current_animation()

        # Queue current animation
        self.game.animation_manager.queue_animation(
            self.entity_id,
            current_anim,
            priority=1 if self.is_hurt or self.is_special_attacking else 0,
        )

        # Update animation frame
        frame = self.game.animation_manager.update_animation(
            self.entity_id, dt, self.should_flip()
        )

        # Update particles
        if self.visible:
            self.game.animation_manager.update_particles(
                self.entity_id, dt, self.game.screen
            )

        return frame

    def should_flip(self) -> bool:
        """Determine if sprite should be flipped"""
        return (self.base_facing_left and self.facing_right) or (
            not self.base_facing_left and not self.facing_right
        )

    def load_sprite_sheets(self) -> None:
        """Load character sprite sheets via animation manager"""
        sprite_path = f"assets/sprites/{self.name.lower()}"
        self.game.animation_manager.load_sprite_sheets(
            self.entity_id, self.name, sprite_path
        )
        self.sprites_loaded = True
