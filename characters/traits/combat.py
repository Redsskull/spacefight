import pygame
from typing import Optional
from config import (
    CONTROLS,
    ATTACK_SETTINGS,
    SPECIAL_ATTACK_SETTINGS,
    ANIMATION_SETTINGS,
)


class CombatMixin:
    """Handles character combat mechanics"""

    def __init__(self):
        # Combat properties - Basic Attack
        attack_settings = ATTACK_SETTINGS.get(self.name, ATTACK_SETTINGS["default"])
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = attack_settings["cooldown"]
        self.attack_range = pygame.Surface(attack_settings["range_size"])
        self.attack_range.fill(attack_settings["range_color"])
        self.attack_offset = attack_settings.get("offset", {"x": 0, "y": 0})

        # Combat properties - Special Attack
        self.has_special_attack = False
        self.is_special_attacking = False
        self.special_attack_timer = 0
        self.special_attack_cooldown = SPECIAL_ATTACK_SETTINGS["cooldown"]
        self.projectiles = pygame.sprite.Group()
        self.ranged_attacker = False

    def attack(self, dt: float) -> None:
        """Handle attack inputs and timing"""
        if not hasattr(self, "player_number") or self.player_number is None:
            return

        # Update timers
        if self.attack_timer > 0:
            self.attack_timer -= dt
        if self.special_attack_timer > 0:
            self.special_attack_timer -= dt

        controls = CONTROLS[f"player{self.player_number}"]["combat"]

        # Handle player 1 (mouse) vs player 2 (keyboard) controls
        if self.player_number == 1:
            mouse = pygame.mouse.get_pressed()
            if (
                mouse[controls["attack"] - 1]
                and not self.attacking
                and self.attack_timer <= 0
            ):
                self.start_attack()

        elif self.player_number == 2:
            keys = pygame.key.get_pressed()
            if (
                keys[controls["attack"]]
                and not self.attacking
                and self.attack_timer <= 0
            ):
                self.start_attack()

    def start_attack(self):
        """Start an attack sequence"""
        self.attacking = True
        self.attack_timer = self.attack_cooldown
        if hasattr(self.game, "sound_manager"):
            self.game.sound_manager.play_sound("punch")

    def take_damage(self, amount: int) -> None:
        """Take damage"""
        self.health = max(0, self.health - amount)
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_blink_timer = self.death_blink_duration
            self.animation_complete = False
            self.blink_count = 0

        # Trigger hurt animation if available
        if hasattr(self, "using_sprites") and self.using_sprites and not self.is_dying:
            if "hurt" in self.sprite_sheets:
                self.is_hurt = True
                self.hurt_timer = self.hurt_duration
