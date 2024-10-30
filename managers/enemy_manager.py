import pygame
import random
from enemy import Enemy

class EnemyManager:
    """
    Manages enemy spawning, behavior, and lifecycle.
    Handles enemy spawning, updates, collisions, and cleanup.
    """

    def __init__(self, game):
        """
        Initialize the EnemyManager.
        Args:
            game (Game): The game instance
        """
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.spawn_points = [
            # Left side spawn points
            (-50, 447),
            (-50, 500),
            (-50, 575),
            # Right side spawn points
            (1250, 447),
            (1250, 500),
            (1250, 575),
        ]
        self.spawn_timer = 0
        self.spawn_cooldown = 3.0  # Seconds between spawn attempts
        self.max_enemies = 10

    def update(self, dt):
        """
        Update all enemies and handle spawning
        Args:
            dt (float): Time delta since last update
        """
        # Update spawn timer
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self._try_spawn_enemy()
            self.spawn_timer = self.spawn_cooldown

        # Update enemies
        for enemy in self.enemies:
            enemy.target = self._find_nearest_target(enemy)
            enemy.update(dt)

            # Remove dead enemies
            if enemy.health <= 0:
                enemy.kill()

    def _try_spawn_enemy(self):
        """
        Attempt to spawn a new enemy if conditions are met
        """
        if len(self.enemies) >= self.max_enemies:
            return

        spawn_point = random.choice(self.spawn_points)
        new_enemy = Enemy(self.game, spawn_point)
        self.enemies.add(new_enemy)

    def _find_nearest_target(self, enemy):
        """
        Find the nearest player character to the enemy
        Args:
            enemy (Enemy): The enemy looking for a target
        Returns:
            Character: The nearest player character
        """
        nearest_target = None
        min_distance = float("inf")

        for character in self.game.character_manager.active_characters:
            distance = (character.position - enemy.position).length()
            if distance < min_distance:
                min_distance = distance
                nearest_target = character

        return nearest_target

    def draw(self, screen):
        """
        Draw all enemies and their attack indicators
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        self.enemies.draw(screen)
        # Draw attack indicators if attacking
        for enemy in self.enemies:
            if enemy.attacking:
                attack_rect = enemy.attack_range.get_rect()
                if enemy.facing_right:
                    attack_rect.midleft = (enemy.rect.centerx, enemy.rect.centery)
                else:
                    attack_rect.midright = (enemy.rect.centerx, enemy.rect.centery)
                screen.blit(enemy.attack_range, attack_rect)

    def handle_collision(self, player_attack_rect, player_strength):
        """
        Handle collisions between player attacks and enemies
        Args:
            player_attack_rect (pygame.Rect): The attack hitbox of the player
            player_strength (int): The strength of the player's attack
        """
        for enemy in self.enemies:
            if enemy.rect.colliderect(player_attack_rect):
                enemy.take_damage(player_strength)

    def clear(self):
        """
        Clear all enemies from the game
        """
        self.enemies.empty()

    def get_enemy_count(self):
        """
        Get the current number of enemies
        Returns:
            int: Number of active enemies
        """
        return len(self.enemies)
