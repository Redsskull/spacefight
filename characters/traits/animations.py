"""
handles all sprite and amimation related properties and methods
"""

from typing import Literal
import pygame
import os
import logging
from graphics import Animator, VisualEffects
from config.characters import (
    CHARACTER_SPRITES,
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

        self.ranged_attacker = False  # Add this trait
        self.has_special_attack = False

    def _get_sprite_config(self):
        """Get sprite configuration based on character name"""
        configs = {
            "Regar": REGAR_SPRITE_CONFIG,
            "Susan": SUSAN_SPRITE_CONFIG,
            "Emily": EMILY_SPRITE_CONFIG,
            "Bart": BART_SPRITE_CONFIG,
        }
        return configs.get(self.name)

    def get_current_animation(self) -> str:
        """Get the current animation based on state priority"""
        if self.is_dying:
            return "death"

        # Special attack takes highest priority
        if self.is_special_attacking:
            if self.ranged_attacker and "shoot" in self.sprite_sheets:
                return "shoot"
            elif "kick" in self.sprite_sheets:
                return "kick"

        # Normal attack next
        if self.attacking:
            return "attack"

        # Movement animations
        if self.direction.length() > 0:
            return "walk"

        # Default state - only return idle if available
        if "idle" in self.sprite_sheets:
            return "idle"
        return "walk"  # Default to walk if no idle animation

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

    def load_sprite_sheets(self, sprite_path: str = None) -> None:
        """Load character sprite sheets"""
        if sprite_path is None:
            sprite_path = f"assets/sprites/{self.name.lower()}"

        logging.debug(f"Loading sprites from: {sprite_path}")
        self.sprites_loaded = False
        self.sprite_sheets = {}  # Reset sprite sheets

        for anim_type, info in CHARACTER_SPRITES[self.name].items():
            try:
                sprite_name = info["name"]
                full_path = os.path.join(sprite_path, f"{sprite_name}.png")

                if not os.path.exists(full_path):
                    logging.error(f"Sprite not found: {full_path}")
                    continue

                sprite_surface = pygame.image.load(full_path).convert_alpha()
                if sprite_surface is None:
                    logging.error(f"Failed to load sprite: {full_path}")
                    continue

                self.sprite_sheets[anim_type] = {
                    "surface": sprite_surface,
                    "frames": info["frames"],
                }
                logging.debug(
                    f"Loaded {anim_type} animation with {info['frames']} frames"
                )

            except (pygame.error, KeyError, IOError) as e:
                logging.error(f"Error loading {anim_type} animation: {e}")
                continue

        # Only set sprites_loaded if we loaded at least one animation
        self.sprites_loaded = len(self.sprite_sheets) > 0
        if not self.sprites_loaded:
            logging.error(f"Failed to load any sprites for {self.name}")
