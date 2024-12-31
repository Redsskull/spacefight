"""Screen management system"""

from typing import Dict, Type, Optional
import logging
import pygame
from screens.base import Screen
from game_states import GameState


class ScreenManager:
    def __init__(self, game):
        self.game = game
        self.current_screen: Optional[Screen] = None
        self.previous_screen: Optional[Screen] = None
        self.registered_screens: Dict[GameState, Type[Screen]] = {}

    def register_screen(self, state: GameState, screen_class: Type[Screen]):
        """Register a screen class for a game state"""
        self.registered_screens[state] = screen_class

    def change_screen(self, new_state: GameState, **kwargs):
        """Change to a new screen based on game state"""
        if new_state not in self.registered_screens:
            logging.error(f"No screen registered for state {new_state}")
            return

        # Store previous screen for transitions
        self.previous_screen = self.current_screen

        # Clean up previous screen if it exists
        if self.current_screen:
            self.current_screen.on_exit()

        # Create and initialize new screen
        screen_class = self.registered_screens[new_state]
        self.current_screen = screen_class(self.game)
        self.current_screen.on_enter(**kwargs)

        # Update game state
        self.game.state = new_state

    def handle_events(self, events: list[pygame.event.Event]):
        """Forward events to current screen"""
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self, dt: float):
        """Update current screen"""
        if self.current_screen:
            self.current_screen.update(dt)

    def draw(self):
        """Draw current screen"""
        if self.current_screen:
            self.current_screen.draw()
