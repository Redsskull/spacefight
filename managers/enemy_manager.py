"""Enemy management system"""

import pygame
import random
import logging
from typing import Optional
from config.spawning import ENEMY_SPAWN
from config.enemies import BASE_ENEMY_STATS
from enemies import BasicEnemy
from characters.player_chars import Character


class EnemyManager:
    """Manages enemy spawning, behavior and lifecycle"""

    def __init__(self, game):
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.spawn_points = ENEMY_SPAWN["spawn_points"]
        self.spawn_timer = 0
        self.spawn_cooldown = ENEMY_SPAWN["spawn_cooldown"]
        self.max_enemies = ENEMY_SPAWN["max_enemies"]

    def update(self, dt: float) -> None:
        """Update enemy spawning and behavior"""
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._try_spawn_enemy()
            self.spawn_timer = self.spawn_cooldown

        for enemy in list(self.enemies):
            enemy.target = self._find_nearest_target(enemy)
            enemy.update(dt)
            if enemy.health <= 0 and not enemy.is_dying:
                enemy.is_dying = True
            elif enemy.health <= 0 and enemy.is_dying and enemy.animation_complete:
                enemy.kill()

    def _try_spawn_enemy(self) -> None:
        """Try to spawn a new enemy if under max limit"""
        try:
            if len(self.enemies) < self.max_enemies:
                spawn_point = random.choice(self.spawn_points)
                enemy = BasicEnemy(self.game, spawn_point)
                self.enemies.add(enemy)
        except Exception as e:
            logging.error(f"Failed to spawn enemy: {str(e)}")

    def _find_nearest_target(self, enemy) -> Optional[Character]:
        """Find closest player character to enemy"""
        nearest = None
        min_dist = float("inf")

        for char in self.game.character_manager.active_characters:
            dist = (char.position - enemy.position).length()
            if dist < min_dist:
                min_dist = dist
                nearest = char

        return nearest

    def draw(self, screen: pygame.Surface) -> None:
        """Draw enemies and their UI elements"""
        for enemy in self.enemies:
            enemy.draw(screen)

            # Draw attack range if attacking
            if enemy.attacking:
                attack_rect = enemy.attack_range.get_rect()
                if enemy.facing_right:
                    attack_rect.midleft = enemy.rect.center
                else:
                    attack_rect.midright = enemy.rect.center
                screen.blit(enemy.attack_range, attack_rect)

            # Draw health bar if not dying
            if not enemy.is_dying:
                self._draw_health_bar(screen, enemy)

    def _draw_health_bar(self, screen: pygame.Surface, enemy) -> None:
        """Draw enemy health bar"""
        bar_width = 50
        bar_height = 5
        health_percent = enemy.health / enemy.max_health

        # Background (red)
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (enemy.rect.x, enemy.rect.y - 10, bar_width, bar_height),
        )

        # Foreground (green)
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (enemy.rect.x, enemy.rect.y - 10, bar_width * health_percent, bar_height),
        )

    def handle_collision(self, attack_rect: pygame.Rect, damage: int) -> None:
        """Handle player attack collision with enemies"""
        for enemy in self.enemies:
            if enemy.rect.colliderect(attack_rect):
                enemy.take_damage(damage)

    def clear(self) -> None:
        """Remove all enemies"""
        self.enemies.empty()

    def get_enemy_count(self) -> int:
        """Get number of active enemies"""
        return len(self.enemies)
