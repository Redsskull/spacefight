import pygame
import random
from enemy import Enemy
import logging


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

        # Update enemies and remove those that have completed their death animation
        for enemy in list(
            self.enemies
        ):  # Create a copy of the list to safely modify during iteration
            enemy.target = self._find_nearest_target(enemy)
            enemy.update(dt)

            # Only remove the enemy after death animation completes
            if enemy.health <= 0 and not enemy.is_dying:
                enemy.is_dying = True  # Trigger death animation
            elif (
                enemy.health <= 0 and enemy.is_dying and enemy.animation_complete
            ):  # Add animation_complete check
                enemy.kill()

    def _try_spawn_enemy(self):
        """Attempt to spawn an enemy with error handling."""
        try:
            if len(self.enemies) >= self.max_enemies:
                return
                
            spawn_point = random.choice(self.spawn_points)
            # Pass spawn_point directly to Enemy constructor
            enemy = Enemy(self.game, spawn_point)
            # Position is now set in Enemy.__init__, no need to set it here
            self.enemies.add(enemy)
            
        except (TypeError, ValueError) as e:
            logging.error(f"Failed to spawn enemy: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in enemy spawn: {e}")

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
        Draw all enemies, their attack indicators, and health bars
        Args:
            screen (pygame.Surface): The screen surface to draw on
        """
        for enemy in self.enemies:
            # Draw enemy sprite
            enemy.draw(screen)

            # Draw attack indicator if attacking
            if enemy.attacking:
                attack_rect = enemy.attack_range.get_rect()
                if enemy.facing_right:
                    attack_rect.midleft = (enemy.rect.centerx, enemy.rect.centery)
                else:
                    attack_rect.midright = (enemy.rect.centerx, enemy.rect.centery)
                screen.blit(enemy.attack_range, attack_rect)

            # Draw enemy health bar
            if not enemy.is_dying:
                health_bar_width = 50
                health_bar_height = 5
                health_percentage = enemy.health / enemy.max_health
                current_health_width = health_bar_width * health_percentage

                # Background (red)
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (
                        enemy.rect.x,
                        enemy.rect.y - 10,
                        health_bar_width,
                        health_bar_height,
                    ),
                )

                # Foreground (green)
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (
                        enemy.rect.x,
                        enemy.rect.y - 10,
                        current_health_width,
                        health_bar_height,
                    ),
                )

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