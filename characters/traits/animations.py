"""
handles all sprite and amimation related properties and methods
"""

from typing import Literal, Optional, TYPE_CHECKING
import pygame
import os
import logging
from graphics import Animator, VisualEffects, SpriteLoader
from config.characters import (
    CHARACTER_SPRITES,
    REGAR_SPRITE_CONFIG,
    SUSAN_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
    BART_SPRITE_CONFIG,
)
from config.combat import ATTACK_SETTINGS
from game_states import EnemyState

if TYPE_CHECKING:
    from enemies.base import (
        BaseEnemy,
    )  # Keep BaseEnemy in TYPE_CHECKING to avoid circular import


class AnimationMixin:
    """Handles character animations and sprites"""

    def __init__(self):
        self.current_animation = "walk"  # default animation
        self.animation_frame = 0
        self.using_sprites = False
        self.visible = True

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

        # Special attack takes highest priority for characters
        if hasattr(self, "is_special_attacking") and self.is_special_attacking:
            if self.ranged_attacker and "shoot" in self.sprite_sheets:
                return "shoot"
            elif "kick" in self.sprite_sheets:
                return "kick"

        # Normal attack next
        if self.attacking:
            return "attack"

        # For enemies, use state-based animations
        if hasattr(self, "state"):
            if self.state == EnemyState.PURSUING and hasattr(self, "direction"):
                if self.direction.length() > 0:
                    return "walk"
            return "idle"  # Default for enemies

        # For characters, use movement-based animations
        if hasattr(self, "direction") and self.direction.length() > 0:
            return "walk"

        # Default state - only return idle if available
        if "idle" in self.sprite_sheets:
            return "idle"
        return "walk"  # Default to walk if no idle animation

    def update_animation(self, dt: float):
        try:
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
        except KeyError as e:
            logging.error(f"Animation error: {e}")
            return None

    def should_flip(self) -> bool:
        """Determine if sprite should be flipped"""
        return (self.base_facing_left and self.facing_right) or (
            not self.base_facing_left and not self.facing_right
        )

    def load_sprite_sheets(self, entity_type=None):
        """Load sprite sheets for the entity"""
        # Import here to avoid circular import
        from enemies.base import BaseEnemy

        if isinstance(self, BaseEnemy):
            sprite_sheets = SpriteLoader.load_enemy_sprites(entity_type)
        else:
            sprite_sheets = SpriteLoader.load_character_sprites(self.name)

        if sprite_sheets:
            self.sprite_sheets = sprite_sheets
            self.sprites_loaded = True

    def get_current_frame(self, animation_name: str) -> Optional[pygame.Surface]:
        """Get the current frame of the specified animation"""
        if not self.using_sprites or animation_name not in self.sprite_sheets:
            return None

        sheet = self.sprite_sheets[animation_name]
        frame_width = sheet["surface"].get_width() // sheet["frames"]
        frame_rect = pygame.Rect(
            frame_width * self.animation_frame,
            0,
            frame_width,
            sheet["surface"].get_height(),
        )

        frame = sheet["surface"].subsurface(frame_rect)
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the character and its projectiles"""
        self.projectiles.draw(screen)

        if self.is_dying and self.animation_complete:
            return

        if self.using_sprites and self.visible:
            current_frame = self.get_current_frame(self.current_animation)
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = self.rect.midbottom
                screen.blit(current_frame, frame_rect)

                # Draw attack range only when attacking
                if self.attacking:
                    self._draw_attack_range(screen, frame_rect)

        else:
            # Non-sprite characters
            if self.visible:
                screen.blit(self.image, self.rect)
                if self.attacking:
                    self._draw_attack_range(screen, self.rect)

    def _draw_attack_range(
        self, screen: pygame.Surface, source_rect: pygame.Rect
    ) -> None:
        """Draw the attack range when attacking"""
        attack_rect = self.attack_range.get_rect()
        attack_config = ATTACK_SETTINGS.get(self.name, ATTACK_SETTINGS["default"])

        if "offset" in attack_config:
            if self.facing_right:
                attack_rect.midleft = (source_rect.right, source_rect.centery)
            else:
                attack_rect.midright = (source_rect.left, source_rect.centery)
            screen.blit(self.attack_range, attack_rect)

    def on_animation_complete(self, animation_name: str) -> None:
        """Handle animation completion events"""
        if animation_name in ["attack", "shoot", "kick"]:
            self.attacking = False
            self.is_special_attacking = False
