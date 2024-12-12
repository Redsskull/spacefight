"""Base enemy class implementation"""

import pygame
from enum import Enum
from config.enemies import BASE_ENEMY_STATS, ENEMY_SPRITE_CONFIG, ENEMY_SPRITES
from config.combat import ENEMY_ATTACK
from characters.base import BaseCharacter


class EnemyState(Enum):
    """Enemy AI states"""

    SPAWNING = "spawning"
    PURSUING = "pursuing"
    ATTACKING = "attacking"
    STUNNED = "stunned"


class BaseEnemy(BaseCharacter):
    """Base class for enemy types"""

    def __init__(self, game, spawn_position, enemy_type="basic"):
        super().__init__("Enemy", game)

        # Load stats from config
        self.health = BASE_ENEMY_STATS["health"]
        self.speed = BASE_ENEMY_STATS["speed"]
        self.strength = BASE_ENEMY_STATS["strength"]
        self.color = BASE_ENEMY_STATS["color"]

        # Position and state
        self.position = pygame.math.Vector2(spawn_position)
        self.rect.topleft = self.position
        self.state = EnemyState.SPAWNING
        self.target = None

        # Sprite settings
        self.sprite_config = ENEMY_SPRITE_CONFIG
        self.sprite_data = ENEMY_SPRITES[enemy_type]
        self.base_facing_left = True  # Enemies face left by default
        self.facing_right = False  # Will be updated based on target position

        # Attack properties
        self.attack_range_distance = ENEMY_ATTACK["range_distance"]
        self.attack_range = pygame.Surface(ENEMY_ATTACK["range_size"])
        self.attack_range.fill(ENEMY_ATTACK["range_color"])
        self.attack_cooldown = ENEMY_ATTACK["cooldown"]
        self.attack_timer = 0
        self.attacking = False

        # Stun properties
        self.stun_duration = BASE_ENEMY_STATS["stun_duration"]
        self.stun_timer = 0

        # Death animation
        self.death_blink_speed = BASE_ENEMY_STATS["death_blink_speed"]
        self.death_duration = BASE_ENEMY_STATS["death_duration"]
        self.death_blink_duration = BASE_ENEMY_STATS["death_blink_duration"]
        self.death_total_time = BASE_ENEMY_STATS["death_total_time"]
        self.max_blinks = BASE_ENEMY_STATS["max_blinks"]

    def update_facing(self):
        """Update enemy facing direction based on target position"""
        if self.target:
            # Face right if target is to the right
            self.facing_right = self.target.position.x > self.position.x
