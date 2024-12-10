"""
Base class for all screens in the game.
"""

import pygame


class Screen:
    """
    Base class for all screens in the game.
    """

    def __init__(self, game: "Game"):
        """
        Initialize the screen.
        Args:
            game (Game): The game object

        """
        self.game = game
        self.screen = game.screen

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        pass
