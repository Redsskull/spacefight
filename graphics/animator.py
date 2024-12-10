"""
Handles animation state and frame management
"""

from typing import Optional, Dict
import pygame
from config import ANIMATION_SETTINGS


class Animator:
    """Manages animation state transitions and frame updates"""

    def __init__(self):
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = ANIMATION_SETTINGS["frame_duration"]

    def update(
        self, dt: float, sprite_sheets: Dict, should_flip: bool
    ) -> Optional[pygame.Surface]:
        """Update animation state and return current frame"""
        if not sprite_sheets or not self.current_animation:
            return None

        self._update_animation_timing(dt, sprite_sheets)
        return self.get_frame(sprite_sheets, should_flip)

    def _update_animation_timing(self, dt: float, sprite_sheets: Dict) -> None:
        """Update animation frame timing"""
        self.animation_timer += dt
        if self.animation_timer >= self.frame_duration:
            self.animation_timer = 0
            sheet_info = sprite_sheets[self.current_animation]
            total_frames = sheet_info["frames"]
            self.animation_frame = (self.animation_frame + 1) % total_frames

    def get_frame(
        self, sprite_sheets: Dict, should_flip: bool
    ) -> Optional[pygame.Surface]:
        """Get the current animation frame"""
        if not self.current_animation or self.current_animation not in sprite_sheets:
            return None

        sheet = sprite_sheets[self.current_animation]["surface"]
        frames = sprite_sheets[self.current_animation]["frames"]

        # Calculate frame dimensions
        frame_width = sheet.get_width() // frames
        frame_height = sheet.get_height()

        # Extract current frame
        frame_x = self.animation_frame * frame_width
        frame = sheet.subsurface((frame_x, 0, frame_width, frame_height))

        # Handle flipping
        if should_flip:
            frame = pygame.transform.flip(frame, True, False)

        return frame
