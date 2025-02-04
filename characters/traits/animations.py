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
from config.graphics import ANIMATION_SETTINGS
from game_states import EnemyState

if TYPE_CHECKING:
    from enemies.base import (
        BaseEnemy,
    )  # Keep BaseEnemy in TYPE_CHECKING to avoid circular import


class AnimationMixin:
    """Handles character animations and sprites"""

    def __init__(self):
        # Animation timing
        self.animation_timer = 0  # Add this
        self.frame_duration = ANIMATION_SETTINGS["frame_duration"]

        # Animation state
        self.current_animation = "walk"  # default animation
        self.animation_frame = 0
        self.using_sprites = False
        self.visible = True

        # Animation components
        self.animator = Animator()
        self.effects = VisualEffects()
        self.sprite_sheets = {}

        # State flags
        self.sprites_loaded = False
        self.is_dying = False
        self.is_hurt = False

        # Register with animation manager
        self.entity_id = id(self)
        self.game.animation_manager.register_entity(
            self.entity_id, self._get_sprite_config()
        )

        # Combat animation states
        self.ranged_attacker = False
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
        """Get the current animation state"""
        if self.is_dying:
            return "death"
        if self.is_special_attacking:
            return "shoot" if self.ranged_attacker else "kick"
        if self.attacking:
            return "attack"
        if self.direction.length() > 0:
            return "walk"

        # Check if character has idle animation, fallback to walk if not
        if "idle" in CHARACTER_SPRITES.get(self.name, {}):
            return "idle"
        return "walk"

    def update_animation(self, dt: float) -> None:
        """Update the animation state"""
        if not self.using_sprites:
            return

        animation_key = self.get_current_animation()
        if animation_key not in self.sprite_sheets:
            return

        # Update animation timer
        self.animation_timer += dt

        # Use character-specific frame duration if available, otherwise use default
        frame_duration = CHARACTER_SPRITES[self.name][animation_key].get(
            "frame_duration", ANIMATION_SETTINGS["frame_duration"]
        )

        if self.animation_timer >= frame_duration:
            self.animation_timer = 0
            total_frames = CHARACTER_SPRITES[self.name][animation_key]["frames"]
            self.animation_frame = (self.animation_frame + 1) % total_frames

            # Reset attack states when animation completes
            if self.attacking and self.animation_frame == 0:
                self.attacking = False
            if self.is_special_attacking and self.animation_frame == 0:
                self.is_special_attacking = False

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
        if not self.sprite_sheets or animation_name not in self.sprite_sheets:
            return None

        sheet = self.sprite_sheets[animation_name]
        frame_width = sheet["surface"].get_width() // sheet["frames"]
        frame_rect = pygame.Rect(
            frame_width * self.animation_frame,
            0,
            frame_width,
            sheet["surface"].get_height(),
        )

        try:
            frame = sheet["surface"].subsurface(frame_rect)
            # Use should_flip() instead of direct facing_right check
            if self.should_flip():
                frame = pygame.transform.flip(frame, True, False)
            return frame
        except ValueError:
            logging.error(
                f"Invalid frame rectangle for {self.name}/{animation_name}: {frame_rect}"
            )
            return None

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the character"""
        # Draw projectiles first
        self.projectiles.draw(screen)

        if not self.visible:
            return

        if self.using_sprites:
            current_frame = self.get_current_frame(self.get_current_animation())
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = self.rect.midbottom
                screen.blit(current_frame, frame_rect)

                # Draw attack range if attacking
                if self.attacking:
                    attack_rect = self.attack_range.get_rect()
                    attack_config = ATTACK_SETTINGS.get(
                        self.name, ATTACK_SETTINGS["default"]
                    )

                    # Create surface with alpha support
                    attack_surface = pygame.Surface(
                        attack_config["range_size"], pygame.SRCALPHA
                    )
                    attack_surface.fill(attack_config["range_color"])

                    if "offset" in attack_config:
                        offset_x = attack_config["offset"]["x"]
                        offset_y = attack_config["offset"]["y"]

                        if self.facing_right:
                            attack_rect.midleft = (self.rect.right, self.rect.centery)
                        else:
                            attack_rect.midright = (self.rect.left, self.rect.centery)

                        screen.blit(attack_surface, attack_rect)
        else:
            # Non-sprite drawing
            self.image.fill(self.color)
            screen.blit(self.image, self.rect)

            if self.attacking:
                attack_rect = self.attack_range.get_rect()
                if self.facing_right:
                    attack_rect.midleft = self.rect.midright
                else:
                    attack_rect.midright = self.rect.midleft
                screen.blit(self.attack_range, attack_rect)

    def _draw_attack_range(
        self, screen: pygame.Surface, source_rect: pygame.Rect
    ) -> None:
        """Draw the attack range when attacking"""
        # Early return to skip drawing attack range
        if self.using_sprites:
            return

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
