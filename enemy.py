import pygame
import random
from enum import Enum
from characters import Character


class EnemyState(Enum):
    SPAWNING = 1
    PURSUING = 2
    ATTACKING = 3
    STUNNED = 4


class Enemy(Character):
    """Enhanced enemy class with AI behavior"""

    def __init__(self, game, spawn_position):
        super().__init__("Enemy", health=50, speed=150, strength=5, game=game)
        self.color = (255, 165, 0)  # Orange color for enemy
        self.image.fill(self.color)
        self.position = pygame.math.Vector2(spawn_position)
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        self.state = EnemyState.SPAWNING
        self.target = None
        self.attack_range = 60  # pixels
        self.stun_duration = 0.5  # seconds
        self.stun_timer = 0

    def update(self, dt):
        """Update enemy behavior based on current state"""
        if self.state == EnemyState.STUNNED:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.state = EnemyState.PURSUING
            return

        # Check if enemy is outside the screen, and move it towards the screen
        if self.position.x < self.game.current_screen.left_x:
            self.position.x += self.speed * dt
        elif self.position.x > self.game.current_screen.right_x:
            self.position.x -= self.speed * dt
        elif self.position.y < self.game.current_screen.floor_y - self.rect.height:
            self.position.y += self.speed * dt
        elif self.position.y > self.game.current_screen.ceiling_y:
            self.position.y -= self.speed * dt
        else:
            # Enemy is now inside the screen, switch to pursuing state
            self.state = EnemyState.PURSUING

        if self.state == EnemyState.PURSUING:
            self._pursue_target(dt)
        elif self.state == EnemyState.ATTACKING:
            self._perform_attack(dt)

        # Update position and sprite
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        self.update_sprite()

    def _pursue_target(self, dt):
        """Move towards the nearest player character"""
        if not self.target:
            return

        # Calculate direction to target
        direction = pygame.math.Vector2(
            self.target.position.x - self.position.x,
            self.target.position.y - self.position.y,
        )

        if direction.length() > 0:
            direction = direction.normalize()
            self.facing_right = direction.x > 0

            # Move towards target
            if direction.length() > self.attack_range:
                self.position += direction * self.speed * dt
            else:
                self.state = EnemyState.ATTACKING

    def _perform_attack(self, dt):
        """Perform attack when in range"""
        if not self.target:
            return

        distance = (self.target.position - self.position).length()
        if distance <= self.attack_range:
            if not self.attacking and self.attack_timer <= 0:
                self.attacking = True
                self.attack_timer = self.attack_cooldown
                # TODO: Implement damage dealing to target
                print(f"Enemy attacking {self.target.name}")
        else:
            self.state = EnemyState.PURSUING

        if self.attack_timer > 0:
            self.attack_timer -= dt
        else:
            self.attacking = False

    def take_damage(self, amount):
        """Handle enemy taking damage"""
        self.health -= amount
        self.state = EnemyState.STUNNED
        self.stun_timer = self.stun_duration


class EnemyManager:
    """Manages enemy spawning and behavior"""

    def __init__(self, game):
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
        """Update all enemies and handle spawning"""
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
        """Attempt to spawn a new enemy if conditions are met"""
        if len(self.enemies) >= self.max_enemies:
            return

        spawn_point = random.choice(self.spawn_points)
        new_enemy = Enemy(self.game, spawn_point)
        self.enemies.add(new_enemy)

    def _find_nearest_target(self, enemy):
        """Find the nearest player character to the enemy"""
        nearest_target = None
        min_distance = float("inf")

        for character in self.game.character_manager.active_characters:
            distance = (character.position - enemy.position).length()
            if distance < min_distance:
                min_distance = distance
                nearest_target = character

        return nearest_target

    def draw(self, screen):
        """Draw all enemies"""
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
        """Handle collisions between player attacks and enemies"""
        for enemy in self.enemies:
            if enemy.rect.colliderect(player_attack_rect):
                enemy.take_damage(player_strength)
