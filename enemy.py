import pygame
from enum import Enum
from characters import Character

class EnemyState(Enum):
    """Enum for tracking enemy AI states"""
    SPAWNING = 1
    PURSUING = 2
    ATTACKING = 3
    STUNNED = 4

class Enemy(Character):
    """Enhanced enemy class with AI behavior"""

    def __init__(self, game, spawn_position):
        """
        Initialize an enemy
        Args:
            game (Game): The game instance
            spawn_position (tuple): The x,y coordinates where the enemy spawns
        """
        super().__init__("Enemy", health=50, speed=150, strength=5, game=game)
        self.color = (255, 165, 0)  # Orange color for enemy
        self.image.fill(self.color)
        self.position = pygame.math.Vector2(spawn_position)
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        self.state = EnemyState.SPAWNING
        self.target = None
        self.attack_range_distance = 60  # Attack range in pixels
        self.attack_range = pygame.Surface((50, 100))
        self.attack_range.fill((255, 165, 0, 128))  # Semi-transparent orange
        self.stun_duration = 0.5  # seconds
        self.stun_timer = 0
        self.attack_cooldown = 1.0  # seconds
        self.attack_timer = 0
        self.attacking = False

    def update(self, dt):
        """
        Update enemy behavior based on current state
        Args:
            dt (float): Time delta since last update
        """
        # I will first check if dying and call on the super death animation
        if self.is_dying:
            super().update(dt)
            return


        # First handle stun state
        if self.state == EnemyState.STUNNED:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.state = EnemyState.PURSUING
            return

        # Update attack timer
        if self.attack_timer > 0:
            self.attack_timer -= dt

        # Handle state machine
        if self.state == EnemyState.SPAWNING:
            if self._is_outside_screen():
                self._move_towards_screen(dt)
            else:
                self.state = EnemyState.PURSUING
        elif self.state == EnemyState.PURSUING:
            self._pursue_target(dt)
        elif self.state == EnemyState.ATTACKING:
            self._perform_attack(dt)

        # Update position and sprite
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        self.update_sprite()

    def _is_outside_screen(self):
        """Check if enemy is outside the screen boundaries"""
        return (
            self.position.x < self.game.current_screen.left_x
            or self.position.x > self.game.current_screen.right_x
            or self.position.y < self.game.current_screen.floor_y - self.rect.height
            or self.position.y > self.game.current_screen.ceiling_y
        )

    def _move_towards_screen(self, dt):
        """Move the enemy towards the screen"""
        if self.position.x < self.game.current_screen.left_x:
            self.position.x += self.speed * dt
        elif self.position.x > self.game.current_screen.right_x:
            self.position.x -= self.speed * dt

        if self.position.y < self.game.current_screen.floor_y - self.rect.height:
            self.position.y += self.speed * dt
        elif self.position.y > self.game.current_screen.ceiling_y:
            self.position.y -= self.speed * dt

    def _pursue_target(self, dt):
        """Move towards the nearest player character"""
        if not self.target:
            return

        # Calculate direction to target
        direction = pygame.math.Vector2(
            self.target.position.x - self.position.x,
            self.target.position.y - self.position.y,
        )

        # Calculate distance to target
        distance = direction.length()

        if distance > 0:
            direction = direction.normalize()
            self.facing_right = direction.x > 0

            # If within attack range, switch to attacking state
            if distance <= self.attack_range_distance:
                self.state = EnemyState.ATTACKING
            else:
                # Move towards target
                self.position += direction * self.speed * dt

    def _perform_attack(self, dt):
        """Perform attack when in range"""
        if not self.target:
            self.state = EnemyState.PURSUING
            return

        distance = (self.target.position - self.position).length()

        # If target moved out of range, switch back to pursuing
        if distance > self.attack_range_distance:
            self.state = EnemyState.PURSUING
            self.attacking = False
            return

        # Perform attack if cooldown is finished
        if not self.attacking and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            # Deal damage to target
            if hasattr(self.target, "take_damage"):
                self.target.take_damage(self.strength)
                print(f"Enemy dealt {self.strength} damage to {self.target.name}")

        # Reset attacking flag when cooldown is done
        if self.attack_timer <= 0:
            if not self.attacking:
                self.attacking = True
                self.attack_timer = self.attack_cooldown
                if hasattr(self.target, "take_damage"):
                    self.target.take_damage(self.strength)
                    print(f"Enemy dealt {self.strength} damage to {self.target.name}")
        else:
            if self.attacking and self.attack_timer <= self.attack_cooldown * 0.3:
                self.attacking = False

    def take_damage(self, amount):
        """
        Handle enemy taking damage
        Args:
            amount (int): Amount of damage to take
        """
        super().take_damage(amount)
        if not self.is_dying:
            self.state = EnemyState.STUNNED
            self.stun_timer = self.stun_duration
        
