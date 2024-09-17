# story_screen.py
import pygame
from .base import Screen
from characters import Regar, Susan, Emily, Bart

class StoryScreen(Screen):
    """
    The story screen where the intro text appears and characters speak.
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
        self.text_box = pygame.Rect(50, 50, self.game.SCREEN_WIDTH - 100, self.game.SCREEN_HEIGHT - 100)

        # Initialize characters
        self.regar = Regar()
        self.susan = Susan()
        self.emily = Emily()
        self.bart = Bart()

         # Define story segments with positions
        self.story_segments = [
            {'character': None, 'text': "Welcome to the SpaceFight story intro.", 'position': (50, 50)},
            {'character': self.regar, 'text': "Regar: I'm very hungry, I stole some food from the kitchen!", 'position': (350, 150)},
            {'character': self.susan, 'text': "Susan: Regar, you're going to get us in trouble!", 'position': (50, 250)},
            {'character': self.emily, 'text': "Bart: Hey little lady, you're looking mighty fine today!", 'position': (350, 350)},
            {'character': self.bart, 'text': "Emily: Grrr, I'm not your little lady!", 'position': (50, 450)},
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

            #Calculate text box size
            self.text_box_width = text_rect.width + 20
            self.text_box_height = text_rect.height + 20

            # Draw text box
            text_box = pygame.Rect(text_rect.x - 10, text_rect.y - 10, self.text_box_width, self.text_box_height)
            pygame.draw.rect(self.screen, (0, 0, 0), text_box)
            pygame.draw.rect(self.screen, (255, 255, 255), text_box, 2)

            # Draw text
            self.screen.blit(text, text_rect)

    def on_resume(self):
        """
        Resume the story screen.
        """
        self.initialize_music()
