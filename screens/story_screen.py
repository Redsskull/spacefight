import pygame
from .base import Screen

class StoryScreen(Screen):
    """
    The story screen where the intro text appears.
    """

    def __init__(self, game):
        """
        Initialize the story screen.
        Args:
            game (Game): The game object
        """
        super().__init__(game)
        self.background = pygame.image.load("assets/spaceship.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )

        self.font = pygame.font.Font(None, 36)

        # Define story segments with positions
        self.story_segments = [
            {'text': "Welcome to the SpaceFight story intro.", 'position': (50, 50)},
            {'text': "Our heroes are about to embark on an epic journey.", 'position': (350, 150)},
            {'text': "But first, let's get to know them a bit better.", 'position': (50, 250)},
            {'text': "They are ready to face whatever challenges come their way.", 'position': (350, 350)},
            {'text': "Let's join them on their adventure!", 'position': (50, 450)},
        ]

        # Initialize music
        self.initialize_music()

        # Track the current story segment
        self.current_segment = 0

    def initialize_music(self):
        """
        Initialize the music for the story screen.
        """
        pygame.mixer.music.load("assets/battlegamenoises.mp3")
        pygame.mixer.music.play(-1)

    def handle_events(self, events):
        """
        Handle events for the story screen.
        Args:
            events (List[Event]): A list of pygame events
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.current_segment += 1
                    if self.current_segment >= len(self.story_segments):
                        from .main_menu import MainMenu  # Import here to avoid circular import
                        self.game.change_screen(MainMenu(self.game))  # Return to main menu after story

    def draw(self):
        """
        Draw the story screen.
        """
        self.screen.blit(self.background, (0, 0))

        # Draw current story segment
        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[self.current_segment]
            text = self.font.render(segment['text'], True, (255, 255, 255))
            text_rect = text.get_rect(topleft=segment['position'])

            # Calculate text box size based on text size
            text_box_width = text_rect.width + 20
            text_box_height = text_rect.height + 20

            # Draw text box
            text_box = pygame.Rect(text_rect.x - 10, text_rect.y - 10, text_box_width, text_box_height)
            pygame.draw.rect(self.screen, (0, 0, 0), text_box)
            pygame.draw.rect(self.screen, (255, 255, 255), text_box, 2)

            # Draw text
            self.screen.blit(text, text_rect)

    def on_resume(self):
        """
        Resume the story screen.
        """
        self.initialize_music()
