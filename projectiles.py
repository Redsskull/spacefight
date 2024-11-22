import pygame
from typing import Tuple, Union
from abc import ABC, abstractmethod


class BaseProjectile(pygame.sprite.Sprite, ABC):
    """Base class for all projectiles in the game"""

    def __init__(
        self,
        pos: Tuple[int, int],
        direction: pygame.math.Vector2,
        damage: int = 10,
        speed: int = 400,
    ):
        super().__init__()
        self.position = pygame.math.Vector2(pos)
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.rect = self.image.get_rect()
        self.rect.center = pos

    @property
    @abstractmethod
    def image(self) -> pygame.Surface:
        """Each projectile type must implement its own image"""
        pass

    def update(self, dt: float) -> None:
        """Update projectile position and check bounds"""
        self.position += self.direction * self.speed * dt
        self.rect.center = self.position
        if self.is_off_screen():
            self.kill()

    def is_off_screen(self) -> bool:
        """Check if projectile is off screen"""
        return (
            self.rect.right < 0 or self.rect.left > 1280
        )  # TODO: Get screen width from config


class EnergyShot(BaseProjectile):
    """Regar's energy projectile"""

    def __init__(self, pos: Tuple[int, int], direction: pygame.math.Vector2, **kwargs):
        self._image = pygame.image.load("assets/sprites/regar/shot.png").convert_alpha()
        super().__init__(pos, direction, **kwargs)

    @property
    def image(self) -> pygame.Surface:
        return self._image
