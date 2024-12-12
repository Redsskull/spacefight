"""
This module contains the Attack class, which handles core attack mechanics and hit detection.
"""

from typing import Tuple
import pygame
from config.combat import ATTACK_SETTINGS


class Attack:
    """Handles core attack mechanics and hit detection"""

    def __init__(
        self, name: str, damage: int, range_size: Tuple[int, int], cooldown: float
    ):
        """
        Initialize the attack
        Args:
            name (str): The name of the attack
            damage (int): The amount of damage the attack deals
            range_size (Tuple[int, int]): The size of the attack range
            cooldown (float): The cooldown of the attack
        """
        attack_config = ATTACK_SETTINGS.get(name, ATTACK_SETTINGS["default"])
        self.name = name
        self.damage = damage or attack_config["damage"]
        self.cooldown = cooldown or attack_config["cooldown"]
        self.range = pygame.Surface(range_size or attack_config["range_size"])
        self.active = False
        self.timer = 0.0

    def update(self, dt: float) -> None:
        """Update attack state and cooldown
        Args:
            dt (float): Time since last frame
        """
        if self.timer > 0:
            self.timer -= dt
            if self.timer <= 0:
                self.active = False

    def trigger(self) -> bool:
        """Attempt to trigger the attack
        Returns:
            bool: True if the attack was successfully triggered, False otherwise
        """
        if self.timer <= 0:
            self.active = True
            self.timer = self.cooldown
            return True
        return False
