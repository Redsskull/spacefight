import pygame
from typing import Tuple, Optional
from abc import ABC, abstractmethod
from config import SCREEN_WIDTH  # Add this import at the top


class ProjectileSystem:
    """Manages projectile lifecycle and collisions"""

    def __init__(self):
        self.active_projectiles = pygame.sprite.Group()

    def update(self, dt: float) -> None:
        """Update all active projectiles"""
        for projectile in self.active_projectiles:
            projectile.update(dt)
            if projectile.is_off_screen():
                projectile.kill()

    def spawn_projectile(
        self,
        projectile_class,
        spawn_pos: Tuple[int, int],
        direction: pygame.math.Vector2,
        **kwargs
    ) -> None:
        """Spawn a new projectile"""
        projectile = projectile_class(spawn_pos, direction, **kwargs)
        self.active_projectiles.add(projectile)

    def clear(self) -> None:
        """Remove all active projectiles"""
        self.active_projectiles.empty()


class BaseProjectile(pygame.sprite.Sprite, ABC):
    """Base class for all projectiles"""

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
        """Update projectile position"""
        self.position += self.direction * self.speed * dt
        self.rect.center = self.position

    def is_off_screen(self) -> bool:
        """Check if projectile is off screen"""
        # Use SCREEN_WIDTH from config instead of hard-coded value
        return self.rect.right < 0 or self.rect.left > SCREEN_WIDTH


class EnergyShot(BaseProjectile):
    """Regar's energy projectile"""

    def __init__(self, pos: Tuple[int, int], direction: pygame.math.Vector2, **kwargs):
        self._image = pygame.image.load("assets/sprites/regar/shot.png").convert_alpha()
        super().__init__(pos, direction, **kwargs)

    @property
    def image(self) -> pygame.Surface:
        return self._image
