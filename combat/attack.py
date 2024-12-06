import pygame
from typing import Optional, Tuple, Dict
from config import ATTACK_SETTINGS


class Attack:
    """Handles core attack mechanics and hit detection"""

    def __init__(
        self, name: str, damage: int, range_size: Tuple[int, int], cooldown: float
    ):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.range = pygame.Surface(range_size)
        self.active = False
        self.timer = 0.0

    def update(self, dt: float) -> None:
        """Update attack state and cooldown"""
        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False

    def trigger(self) -> bool:
        """Attempt to trigger the attack"""
        if self.timer <= 0:
            self.active = True
            self.timer = self.cooldown
            return True
        return False
