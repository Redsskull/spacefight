"""Combat management system"""

from typing import Dict, List, Optional
import pygame
import logging
from characters.player_chars import Character
from enemies import BaseEnemy
from combat.attack import Attack
from combat.damage import DamageSystem
from combat.projectiles import ProjectileSystem
from config.combat import ATTACK_SETTINGS, SPECIAL_ATTACK_SETTINGS
from managers.enemy_manager import EnemyManager


class CombatManager:
    """Manages combat interactions, collisions and state tracking"""

    def __init__(self, game):
        """Initialize combat management system"""
        self.game = game
        self.damage_system = DamageSystem()
        self.projectile_system = ProjectileSystem()

        # Combat state tracking
        self.active_attacks: Dict[int, Attack] = {}
        self.attack_collisions: List[pygame.Rect] = []

    def update(self, dt: float) -> None:
        """Update combat state and check collisions"""
        self.projectile_system.update(dt)
        self._check_projectile_collisions()
        self._check_melee_collisions()
        self._update_attack_states(dt)

    def _check_projectile_collisions(self) -> None:
        """Check projectile collisions with enemies"""
        for projectile in list(self.projectile_system.active_projectiles):
            for enemy in self.game.enemy_manager.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    damage = self.damage_system.calculate_damage(
                        projectile.damage, "Regar", "Enemy"
                    )
                    # Use take_damage instead of direct health modification
                    enemy.take_damage(damage)
                    projectile.kill()

    def _check_melee_collisions(self) -> None:
        """Check melee attack collisions using the original system"""
        for character in self.game.character_manager.active_characters:
            if character.attacking:
                attack_rect = character.attack_range.get_rect()
                if character.facing_right:
                    attack_rect.midleft = character.rect.midright
                else:
                    attack_rect.midright = character.rect.midleft

                # Let enemy manager handle collisions
                self.game.enemy_manager.handle_collision(
                    attack_rect, character.strength
                )
                self.attack_collisions.append(attack_rect)

    def _get_attack_rect(self, character: Character) -> Optional[pygame.Rect]:
        """Get attack hitbox rectangle based on character facing and offset"""
        if not character.attacking:
            return None

        attack_settings = ATTACK_SETTINGS.get(
            character.name, ATTACK_SETTINGS["default"]
        )
        attack_rect = pygame.Rect((0, 0), attack_settings["range_size"])
        offset = attack_settings.get("offset", {"x": 0, "y": 0})

        if character.facing_right:
            attack_rect.midleft = (
                character.rect.right + offset["x"],
                character.rect.centery + offset["y"],
            )
        else:
            attack_rect.midright = (
                character.rect.left - offset["x"],
                character.rect.centery + offset["y"],
            )

        return attack_rect

    def _update_attack_states(self, dt: float) -> None:
        """Update active attacks and cooldowns"""
        for entity_id, attack in list(self.active_attacks.items()):
            attack.update(dt)
            if not attack.active:
                del self.active_attacks[entity_id]

    def register_attack(self, entity_id: int, attack: Attack) -> None:
        """Register a new attack instance"""
        self.active_attacks[entity_id] = attack

    def handle_enemy_attack(self, enemy: "BaseEnemy", target: "Character") -> None:
        """Handle enemy attack using the original system"""
        if enemy.attacking and enemy.attack_timer <= 0:
            enemy.attack_timer = enemy.attack_cooldown

            # Use direct damage application like in the original
            if hasattr(target, "take_damage"):
                damage = self.damage_system.calculate_damage(
                    enemy.strength, "Enemy", target.name
                )
                target.take_damage(damage)

    def handle_special_attack(self, character: Character) -> None:
        """Handle special attack execution based on character's implementation"""
        if (
            character.has_special_attack
            and hasattr(character, "perform_special_attack")
            and not character.special_attack_timer > 0
        ):
            # Let the character handle its own special attack logic
            character.perform_special_attack()

    def clear(self) -> None:
        """Clear all combat states"""
        self.active_attacks.clear()
        self.projectile_system.clear()
        self.attack_collisions.clear()
