import pytest
import pygame
from combat.attack import Attack
from combat.damage import DamageSystem
from combat.projectiles import ProjectileSystem, BaseProjectile, EnergyShot


def test_attack_system():
    """Test basic attack mechanics"""
    # Initialize attack
    attack = Attack("punch", 10, (50, 50), 0.5)

    # Test initial state
    assert not attack.active
    assert attack.timer == 0

    # Test attack triggering
    assert attack.trigger() == True  # Should succeed
    assert attack.active
    assert attack.timer == 0.5

    # Test cooldown
    assert attack.trigger() == False  # Should fail during cooldown

    # Test cooldown expiration
    attack.update(0.6)  # Update past cooldown
    assert attack.timer <= 0
    assert not attack.active
    assert attack.trigger() == True  # Should succeed again


def test_attack_hit_detection():
    """Test attack hit detection between attacker and target"""
    pygame.init()

    # Setup attack with hit box
    attack = Attack("punch", 10, (50, 50), 0.5)
    attack_pos = pygame.math.Vector2(100, 100)

    # Create target rect
    target_rect = pygame.Rect(90, 90, 40, 40)

    # Test hit detection
    attack.trigger()

    # Check if attack hitbox overlaps target
    attack_rect = attack.range.get_rect(center=attack_pos)
    assert attack_rect.colliderect(target_rect)


def test_energy_shot():
    """Test EnergyShot projectile behavior"""
    pygame.init()

    # Test creation
    pos = (100, 100)
    direction = pygame.math.Vector2(1, 0)  # Moving right
    shot = EnergyShot(pos, direction, damage=15, speed=500)

    # Test properties
    assert shot.damage == 15
    assert shot.speed == 500
    assert shot.rect.center == pos

    # Test movement
    dt = 0.016  # Simulate one frame at ~60fps
    initial_x = shot.position.x
    shot.update(dt)
    assert shot.position.x > initial_x

    # Test off-screen detection
    shot.position.x = 1300  # Move beyond screen width
    shot.rect.center = shot.position
    shot.rect.update(
        shot.position.x, shot.position.y, shot.rect.width, shot.rect.height
    )  # Ensure rect is updated
    assert shot.is_off_screen()


def test_projectile_system():
    """Test ProjectileSystem management"""
    pygame.init()

    system = ProjectileSystem()

    # Test spawning
    system.spawn_projectile(
        EnergyShot, (100, 100), pygame.math.Vector2(1, 0), damage=15, speed=500
    )
    assert len(system.active_projectiles) == 1

    # Test updating
    projectile = next(iter(system.active_projectiles))
    initial_x = projectile.position.x
    system.update(0.016)
    assert projectile.position.x > initial_x

    # Test cleanup of off-screen projectiles
    projectile.position.x = 1300
    projectile.rect.center = projectile.position
    system.update(0.016)
    assert len(system.active_projectiles) == 0
