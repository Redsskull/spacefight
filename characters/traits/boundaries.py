from typing import Tuple
import pygame


class BoundaryMixin:
    """Handles boundary checking for game entities"""

    def __init__(self):
        self.bounds = {"left": 0, "right": 1280, "top": 0, "bottom": 720}

    def set_boundaries(self, left: int, right: int, top: int, bottom: int) -> None:
        """Set boundary limits"""
        self.bounds = {"left": left, "right": right, "top": top, "bottom": bottom}

    def check_boundaries(
        self, position: pygame.math.Vector2
    ) -> Tuple[bool, pygame.math.Vector2]:
        """Check if position is within boundaries and return corrected position"""
        corrected = pygame.math.Vector2(position)

        if position.x < self.bounds["left"]:
            corrected.x = self.bounds["left"]
        elif position.x > self.bounds["right"]:
            corrected.x = self.bounds["right"]

        if position.y < self.bounds["top"]:
            corrected.y = self.bounds["top"]
        elif position.y > self.bounds["bottom"]:
            corrected.y = self.bounds["bottom"]

        return position != corrected, corrected
