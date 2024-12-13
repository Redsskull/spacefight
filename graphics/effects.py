"""
Handles visual effects like death animation and hurt states
"""

from typing import List, Tuple
import random
import pygame
from config.graphics import ANIMATION_SETTINGS


class VisualEffects:
    """Manages visual effects for characters"""

    def __init__(self):
        # Death effect properties
        self.is_dying = False
        self.death_blink_duration = ANIMATION_SETTINGS["death"]["blink_duration"]
        self.death_total_time = ANIMATION_SETTINGS["death"]["total_time"]
        self.death_blink_timer = self.death_blink_duration
        self.blink_count = 0
        self.max_blinks = ANIMATION_SETTINGS["death"]["max_blinks"]
        self.animation_complete = False

        # Hurt effect properties
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = ANIMATION_SETTINGS["frame_duration"]

        # Particle system properties
        self.particles: List[dict] = []
        self.impact_particles: List[dict] = []

    def update_death_effect(self, dt: float, sprite: pygame.Surface) -> bool:
        """Update death animation effect"""
        if not self.is_dying:
            return False

        self.death_total_time -= dt
        self.death_blink_timer -= dt

        if self.death_blink_timer <= 0:
            self.death_blink_timer = self.death_blink_duration
            self.blink_count += 1  # Make sure this increment happens
            return True  # Return True when a blink occurs

        return False

    def update_hurt_effect(self, dt: float) -> None:
        """Update hurt state effect"""
        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False

    def add_particle_effect(
        self, position: Tuple[float, float], color: Tuple[int, int, int]
    ):
        """Add particle effects"""
        for _ in range(10):  # Number of particles
            self.particles.append(
                {
                    "pos": pygame.math.Vector2(position),
                    "vel": pygame.math.Vector2().rotate(random.randint(0, 360)),
                    "color": color,
                    "lifetime": 1.0,
                    "size": 3,
                }
            )

    def handle_impact_effect(self, position: Tuple[float, float]):
        """Handle impact visualization"""
        for _ in range(5):  # Number of impact particles
            self.impact_particles.append(
                {
                    "pos": pygame.math.Vector2(position),
                    "vel": pygame.math.Vector2().rotate(random.randint(-45, 45)),
                    "lifetime": 0.3,
                    "size": 5,
                }
            )

    def update_particles(self, dt: float, surface: pygame.Surface):
        """Update and draw particles"""
        # Update regular particles
        for particle in self.particles[:]:
            particle["lifetime"] -= dt
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                continue

            particle["pos"] += particle["vel"] * dt * 60
            particle["size"] *= 0.95

            # Draw particle
            pygame.draw.circle(
                surface, particle["color"], particle["pos"], int(particle["size"])
            )

        # Update impact particles
        for particle in self.impact_particles[:]:
            particle["lifetime"] -= dt
            if particle["lifetime"] <= 0:
                self.impact_particles.remove(particle)
                continue

            particle["pos"] += particle["vel"] * dt * 120

            # Draw impact particle
            pygame.draw.circle(
                surface, (255, 255, 255), particle["pos"], int(particle["size"])
            )
