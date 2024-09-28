import random
import pygame

class ScreenEffectsManager:
    """
    Manages visual effects like screen shaking.
    """

    def __init__(self, screen, screen_width, screen_height):
        """
        Initialize the ScreenEffectsManager.
        Args:
            screen (pygame.Surface): The screen surface.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.shake_duration = 0
        self.shake_intensity = 0
        self.shake_start_time = 0
        self.shaking = False

    def start_shake(self, duration, intensity):
        """
        Start the screen shake effect.
        Args:
            duration (int): Duration of the shake in milliseconds.
            intensity (int): Intensity of the shake in pixels.
        """
        self.shake_duration = duration
        self.shake_intensity = intensity
        self.shake_start_time = pygame.time.get_ticks()
        self.shaking = True

    def update(self):
        """
        Update the screen shake effect.
        """
        if self.shaking:
            current_time = pygame.time.get_ticks()
            if current_time - self.shake_start_time > self.shake_duration:
                self.shaking = False

    def apply_shake(self):
        """
        Apply the screen shake effect to the screen.
        """
        if self.shaking:
            dx = random.randint(-self.shake_intensity, self.shake_intensity)
            dy = random.randint(-self.shake_intensity, self.shake_intensity)
            self.screen.blit(self.screen, (dx, dy))
