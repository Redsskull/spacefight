"""Base enemy class implementation"""

import pygame
from enum import Enum
from config.enemies import (
    BASE_ENEMY_STATS,
    ENEMY_SPRITE_CONFIG,
    ENEMY_SPRITES,
)
from config.combat import ENEMY_ATTACK
from config.graphics import ANIMATION_SETTINGS
from characters.base import BaseCharacter
from game_states import EnemyState
from characters.traits import AnimationMixin, CombatMixin
from graphics import SpriteLoader


class BaseEnemy(pygame.sprite.Sprite, CombatMixin, AnimationMixin):
    """Base class for enemy types"""

    def __init__(self, game, spawn_position, enemy_type="basic"):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Enemy"
        self.game = game

        # Make sure rect is properly positioned
        self.position = pygame.math.Vector2(spawn_position)
        self.image = pygame.Surface((50, 100))
        self.image.fill(BASE_ENEMY_STATS["color"])
        self.rect = self.image.get_rect()
        self.rect.topleft = spawn_position  # This is crucial

        # Initialize combat after setting position
        CombatMixin.__init__(self)
        AnimationMixin.__init__(self)

        self.sprite_config = ENEMY_SPRITE_CONFIG
        self.sprite_data = ENEMY_SPRITES[enemy_type]
        self.direction = pygame.math.Vector2()  # Add direction vector for animation

        # Create initial image and rect (needed for collision detection)
        self.image = pygame.Surface((50, 100))  # Default size
        self.image.fill(BASE_ENEMY_STATS["color"])
        self.rect = self.image.get_rect()

        # Load stats from config
        self.health = BASE_ENEMY_STATS["health"]
        self.max_health = BASE_ENEMY_STATS["health"]
        self.speed = BASE_ENEMY_STATS["speed"]
        self.strength = BASE_ENEMY_STATS["strength"]
        self.color = BASE_ENEMY_STATS["color"]

        # Animation timings
        self.hurt_duration = ANIMATION_SETTINGS["frame_duration"]
        self.hurt_timer = 0
        self.is_hurt = False

        # Position and state
        self.position = pygame.math.Vector2(spawn_position)
        self.rect.topleft = spawn_position  # Set initial position
        self.state = EnemyState.SPAWNING
        self.target = None

        # Set up sprites and animations
        self.using_sprites = True
        self.base_facing_left = True
        self.facing_right = False

        # Load sprites through AnimationMixin
        self.load_sprite_sheets(enemy_type)

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

    def take_damage(self, amount: int) -> None:
        """Take damage and handle death/hurt states"""
        # Use the combat mixin's take_damage implementation
        CombatMixin.take_damage(self, amount)

        # Add enemy-specific behavior (stun)
        if not self.is_dying:
            self.state = EnemyState.STUNNED
            self.stun_timer = self.stun_duration
