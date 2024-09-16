import pygame
from .base import Screen


class StoryScreen(Screen):
    def __init__(self, game, story_segments):
        super().__init__(game)
        self.story_segments = story_segments
        self.current_segment = 0
        self.text_surface = None
        self.text_rect = None
        self.text_index = 0  
        self.text_delay = 50  # Delay between each character appearing
        self.last_update = pygame.time.get_ticks()

    def draw_text(self, text, font, color, x, y):
        self.text_surface = font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(
            topleft=(x, y)
        )  # Corrected typo here
        self.screen.blit(self.text_surface, self.text_rect)

    def update_text(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.text_delay:
            self.text_index += 1  # Corrected typo here
            self.last_update = current_time

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[
                self.current_segment
            ]  
            character = segment["character"]
            text = segment["text"]

            # Draw character
            self.screen.blit(character.image, (50, 50))  # Corrected typo here

            # Draw text
            if self.text_index < len(text):
                self.update_text()
                self.draw_text(
                    text[: self.text_index],
                    pygame.font.Font(None, 36),
                    (255, 255, 255),
                    200,
                    100,
                )
            else:
                self.draw_text(
                    text, pygame.font.Font(None, 36), (255, 255, 255), 200, 100
                )

    def handle_events(self, events):  
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.text_index < len(
                        self.story_segments[self.current_segment]["text"]
                    ):
                        self.text_index = len(
                            self.story_segments[self.current_segment]["text"]
                        )
                    else:
                        self.current_segment += 1
                        self.text_index = 0

    def update(self):
        if self.current_segment >= len(self.story_segments):
            # Transition to the next screen (e.g., game screen)
            # For  just print a message
            print("Story complete. Transition to game screen.")
