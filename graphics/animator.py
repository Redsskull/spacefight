"""Handles animation state and frame management"""

from typing import Optional, Dict, List
import pygame
from config.graphics import ANIMATION_SETTINGS


class Animator:
    """Manages animation state transitions and frame updates"""

    def __init__(self):
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = ANIMATION_SETTINGS["frame_duration"]

        # State machine properties
        self.state_machine = {}  # Maps states to valid transitions
        self.animation_queue = []  # Priority queue for animations
        self.can_interrupt = True
        self.is_transitioning = False

    def queue_animation(self, animation_name: str, priority: int = 0):
        """Add animation to queue with priority"""
        if not self.can_interrupt and self.current_animation:
            return

        # Only queue if different from current
        if animation_name != self.current_animation:
            self.animation_queue.append((priority, animation_name))
            self.animation_queue.sort(reverse=True)  # Higher priority first

    def update(
        self, dt: float, sprite_sheets: Dict, should_flip: bool
    ) -> Optional[pygame.Surface]:
        """Update animation state and return current frame"""
        if not sprite_sheets or not self.current_animation:
            return None

        # Handle animation queue
        if self.animation_queue and not self.is_transitioning:
            _, next_animation = self.animation_queue[0]
            if self._can_transition_to(next_animation):
                self.current_animation = next_animation
                self.animation_frame = 0
                self.animation_queue.pop(0)

        # Update timing
        self._update_animation_timing(dt, sprite_sheets)
        return self.get_frame(sprite_sheets, should_flip)

    def _update_animation_timing(self, dt: float, sprite_sheets: Dict) -> None:
        """Update animation frame timing"""
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            sheet_info = sprite_sheets[self.current_animation]
            total_frames = sheet_info["frames"]

            # Handle frame progression
            if self.animation_frame < total_frames - 1:
                self.animation_frame += 1
            else:
                # Animation complete
                self.animation_frame = 0
                if self.animation_queue:
                    _, next_anim = self.animation_queue.pop(0)
                    self.current_animation = next_anim

    def get_frame(
        self, sprite_sheets: Dict, should_flip: bool
    ) -> Optional[pygame.Surface]:
        """Get the current animation frame"""
        if not self.current_animation or self.current_animation not in sprite_sheets:
            return None

        sheet = sprite_sheets[self.current_animation]
        surface = sheet["surface"]
        frames = sheet["frames"]

        # Calculate frame dimensions
        frame_width = surface.get_width() // frames
        frame_height = surface.get_height()

        # Extract frame
        frame_rect = pygame.Rect(
            self.animation_frame * frame_width, 0, frame_width, frame_height
        )
        frame = surface.subsurface(frame_rect).copy()

        # Handle flipping
        if should_flip:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def _can_transition_to(self, new_animation: str) -> bool:
        """Check if transition to new animation is valid"""
        if not self.state_machine:  # If no restrictions defined
            return True

        if self.current_animation not in self.state_machine:
            return True

        return new_animation in self.state_machine[self.current_animation]
