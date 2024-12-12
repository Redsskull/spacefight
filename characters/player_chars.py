"""
This module contains the player characters for the game.
"""

import pygame
from config.characters import CHARACTER_STATS, CHARACTER_SPRITES
from config.combat import ATTACK_SETTINGS, SPECIAL_ATTACK_SETTINGS
from config.graphics import SPRITE_SETTINGS, ANIMATION_SETTINGS
from combat.projectiles import EnergyShot
from .base import BaseCharacter
from .traits.movement import MovementMixin
from .traits.combat import CombatMixin
from .traits.animations import AnimationMixin


class Character(BaseCharacter, MovementMixin, CombatMixin, AnimationMixin):
    """
    Base class combining all character functionality
    Args:
        BaseCharacter (BaseCharacter): Base class for all characters
        MovementMixin (MovementMixin): Mixin for character movement
        CombatMixin (CombatMixin): Mixin for character combat
        AnimationMixin (AnimationMixin): Mixin for character animations
    """

    def __init__(self, name: str, game: "Game"):
        """
        Initialize the character
        Args:
            name (str): The name of the character
            game (Game): The game instance
        """
        BaseCharacter.__init__(self, name, game)
        MovementMixin.__init__(self)
        CombatMixin.__init__(self)
        AnimationMixin.__init__(self)


class Regar(Character):
    """Regar character class"""

    def __init__(self, game):
        """
        Initialize the Regar character
        Args:
            game (Game): The game instance
        """
        super().__init__("Regar", game)
        self.ranged_attacker = True
        self.has_special_attack = True

    def perform_special_attack(self):
        """Perform Regar's energy shot attack"""
        if self.special_attack_timer <= 0:
            self.is_special_attacking = True
            self.animation_timer = 0

            # Create projectile
            direction = (
                pygame.math.Vector2(1, 0)
                if self.facing_right
                else pygame.math.Vector2(-1, 0)
            )
            spawn_x = self.rect.right if self.facing_right else self.rect.left

            projectile = EnergyShot(
                pos=(spawn_x, self.rect.centery),
                direction=direction,
                damage=self.strength,
            )
            self.projectiles.add(projectile)

            # Set cooldown
            self.special_attack_timer = self.special_attack_cooldown

            # Play sound
            if hasattr(self.game, "sound_manager"):
                self.game.sound_manager.play_sound("shoot")


class Susan(Character):
    """Susan character class - Focused on analytical combat"""

    def __init__(self, game):
        super().__init__("Susan", game)
        self.has_special_attack = False  # Susan relies on precise normal attacks

    # Susan doesn't have a special attack - relies on normal combat


class Emily(Character):
    """Emily character class - Engineering specialist with powerful kick"""

    def __init__(self, game):
        super().__init__("Emily", game)
        self.has_special_attack = True

    def perform_special_attack(self):
        """Perform Emily's special kick attack"""
        if self.special_attack_timer <= 0:
            self.is_special_attacking = True
            self.animation_timer = 0

            # Create kick hitbox and calculate position
            kick_config = SPECIAL_ATTACK_SETTINGS["Emily"]
            kick_rect = pygame.Rect(
                0, 0, kick_config["range"]["width"], kick_config["range"]["height"]
            )

            # Position kick hitbox
            if self.facing_right:
                kick_rect.midleft = (
                    self.rect.right + kick_config["offset"]["x"],
                    self.rect.centery + kick_config["offset"]["y"],
                )
            else:
                kick_rect.midright = (
                    self.rect.left - kick_config["offset"]["x"],
                    self.rect.centery + kick_config["offset"]["y"],
                )

            # Check for enemy hits
            for enemy in self.game.enemy_manager.enemies:
                if kick_rect.colliderect(enemy.rect):
                    enemy.take_damage(kick_config["damage"])

            # Set cooldown
            self.special_attack_timer = kick_config["cooldown"]

            # Play sound
            if hasattr(self.game, "sound_manager"):
                self.game.sound_manager.play_sound("kick")


class Bart(Character):
    """Bart character class - Tank character with reversed sprites"""

    def __init__(self, game):
        super().__init__("Bart", game)
        self.base_facing_left = True  # For sprite flipping
        self.facing_right = True  # For initial facing direction
