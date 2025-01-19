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

    def update(self, dt: float) -> None:
        """Update character state"""
        if self.is_dying:
            return

        # Get input state
        if self.player_number:
            keys = pygame.key.get_pressed()
            self.handle_input(keys, dt)

        # Update components
        self.move(dt)
        self.attack(dt)
        self.update_animation(dt)

        # Update projectiles
        for projectile in list(
            self.projectiles
        ):  # Use list to avoid modification during iteration
            projectile.update(dt)
            # Check projectile collisions with enemies
            for enemy in self.game.enemy_manager.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.take_damage(projectile.damage)
                    projectile.kill()
                    break
            # Remove off-screen projectiles
            if projectile.is_off_screen():
                projectile.kill()

    def handle_input(self, keys: list, dt: float) -> None:
        """Handle all input for the character"""
        # Handle movement input
        MovementMixin.handle_input(self, keys, dt)
        # Handle combat input
        CombatMixin.handle_input(self, keys, dt)


class Regar(Character):
    def __init__(self, game):
        super().__init__("Regar", game)
        self.name = "Regar"
        self.ranged_attacker = True  # Regar uses ranged attacks
        self.has_special_attack = True
        self.load_sprite_sheets()

    def perform_special_attack(self):
        """Perform Regar's energy shot attack"""
        if self.special_attack_timer <= 0:
            self.is_special_attacking = True
            self.animation_timer = 0

            # Create projectile with proper direction
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
                speed=400,  # Make sure speed is set
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
    def __init__(self, game):
        super().__init__("Emily", game)
        self.name = "Emily"
        self.has_special_attack = True  # Emily has kick special
        self.load_sprite_sheets()

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
    """Bart character class"""

    def __init__(self, game):
        super().__init__("Bart", game)
        self.base_facing_left = True
        self.facing_right = True

    def move(self, dt: float) -> None:
        """Override to handle Bart's unique facing"""
        super().move(dt)
        if self.direction.x != 0:
            self.facing_right = self.direction.x > 0
