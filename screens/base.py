import pygame


class Screen:
    """
    Base class for all screens in the game.
    """

    def __init__(self, game):
        """
        Initialize the screen.
        Args:
            game (Game): The game object

        """
        self.game = game
        self.screen = game.screen

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

