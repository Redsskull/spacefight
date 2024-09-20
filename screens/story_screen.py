import pygame
import textwrap
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
            {'text': "On the space cargo ship Hyperactive captain by Captain Regar, the skeleton crew make their way to a new uncharted system.", 'position': (50, 50)},
            {'text': "A month ago a myterious order came in to an unknown location.", 'position': (350, 150)},
            {'text': "After much thoght on the matter and a bit of an explorers itch, Regar decided to go.", 'position': (50, 250)},
            {'text': "There will be many challenges along the way", 'position': (350, 350)},
            {'text': "This is the Hypers adventure!", 'position': (50, 450)},
        ]

        # Initialize music
        self.initialize_music()

        # Track the current story segment
        self.current_segment = 0

        # Timer to control text appearance
        self.text_timer = pygame.time.get_ticks()
        self.text_delay = 5000  # 5 seconds delay between text segments
        self.fade_duration = 2000  # 2 seconds for fade in and fade out
        self.fade_timer = 0
        self.fade_direction = 1  # 1 for fade in, -1 for fade out

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
                    self.current_segment = len(self.story_segments)  # Skip to the end

    def update(self):
        """
        Update the story screen.
        """
        current_time = pygame.time.get_ticks()
        if self.current_segment < len(self.story_segments):
            if self.fade_direction == 1:  # Fade in
                self.fade_timer += self.game.clock.get_time()
                if self.fade_timer >= self.fade_duration:
                    self.fade_direction = 0
                    self.fade_timer = self.fade_duration
            elif self.fade_direction == 0:  # Stay
                if current_time - self.text_timer >= self.text_delay:
                    self.fade_direction = -1
                    self.fade_timer = self.fade_duration
            elif self.fade_direction == -1:  # Fade out
                self.fade_timer -= self.game.clock.get_time()
                if self.fade_timer <= 0:
                    self.fade_direction = 1
                    self.fade_timer = 0
                    self.current_segment += 1
                    self.text_timer = current_time

        if self.current_segment >= len(self.story_segments):
            from .main_menu import MainMenu  # Import here to avoid circular import
            self.game.change_screen(MainMenu(self.game))  # Return to main menu after story

    def draw(self):
        """
        Draw the story screen.
        """
        self.screen.blit(self.background, (0, 0))

        # Draw the current story segment
        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[self.current_segment]
            text = segment['text']
            position = segment['position']


            #Wrap the text
            wrapped_text = textwrap.fill(text, width=40)#might need to adjust width

            # Render the wrapped text
            text_lines = wrapped_text.split('\n')
            text_surfaces = [self.font.render(line, True, (255, 255, 255)) for line in text_lines]


            # Calculate the text box size based on wrapped text
            text_box_width = max([text_surface.get_width() for text_surface in text_surfaces]) + 20
            text_box_height = sum([text_surface.get_height() for text_surface in text_surfaces]) + 20

            
            # Draw the text box with fade in/out effect
            alpha = int(self.fade_timer / self.fade_duration * 255)
            text_box_surface = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
            text_box_surface.fill((0, 0, 0, alpha))
            self.screen.blit(text_box_surface,position)


            #Draw the wrapped text with fade effect
            y_offset = 0
            for surface in text_surfaces:
                surface.set_alpha(alpha)
                self.screen.blit(surface, (position[0] + 10, position[1] + 10 + y_offset))
                y_offset += surface.get_height()






    def on_resume(self):
        """
        Resume the story screen.
        """
        self.initialize_music()
