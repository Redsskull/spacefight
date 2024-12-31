import pygame


class Screen:
    """Base class for all game screens"""

    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.initialized = False

    def on_enter(self, **kwargs):
        """Called when entering this screen"""
        if not self.initialized:
            self.initialize()
            self.initialized = True

    def on_exit(self):
        """Called when exiting this screen"""
        pass

    def initialize(self):
        """Called once when screen is first created"""
        pass

    def update(self, dt: float):
        """Update screen logic"""
        pass

    def draw(self):
        """Draw screen content"""
        pass

    def handle_events(self, events: list[pygame.event.Event]):
        """Handle input events"""
        pass
