import pygame
import textwrap
from .base import Screen
from characters import Regar, Susan, Emily, Bart

class StoryScreen(Screen):
    """
    The story screen where the intro text appears and characters interact.
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
        self.intro_segments = [
            {
                "text": "On the space cargo ship Hyperactive captained by Captain Regar, the skeleton crew make their way to a new uncharted system.",
                "position": (50, 50),
            },
            {
                "text": "A month ago a mysterious order came in to an unknown location.",
                "position": (350, 150),
            },
            {
                "text": "After much thought on the matter and a bit of an explorer's itch, Regar decided to go.",
                "position": (50, 250),
            },
            {
                "text": "There will be many challenges along the way",
                "position": (350, 350),
            },
            {"text": "This is the Hyper's adventure!", "position": (50, 450)},
        ]

        self.inside_ship_segments = [
            {"text": "Regar: Alright crew, we're approaching the uncharted system. Everyone on alert!"},
            {"text": "Susan: The engines are running smoothly, Captain."},
            {"text": "Emily: I've plotted the course. We should arrive in a few hours."},
            {"text": "Bart: All systems are green, Captain. We're ready for anything!"}
        ]

        self.story_segments = self.intro_segments

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

        # State variable
        self.state = "intro"

        # Create character instances
        self.characters = [Regar(), Susan(), Emily(), Bart()]

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
            if self.state == "intro":
                self.state = "inside_ship"
                self.story_segments = self.inside_ship_segments
                self.current_segment = 0
            else:
                from .main_menu import MainMenu  # Import here to avoid circular import
                self.game.change_screen(MainMenu(self.game))  # Return to main menu after story

    def draw(self):
        """
        Draw the story screen.
        """
        if self.state == "inside_ship":
            # Clear the screen with a solid color
            self.screen.fill((0, 0, 0))

            self.draw_spaceship_interior()
            self.draw_characters()
            self.draw_current_dialogue()
        else:
            self.screen.blit(self.background, (0, 0))
            self.draw_story_segment()

    def draw_spaceship_interior(self):
        """
        Draw the interior of the spaceship.
        """
        # Draw the main body of the spaceship
        pygame.draw.rect(self.screen, (100, 100, 100), (0, 0, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        
        # Draw windows
        for i in range(3):
            pygame.draw.ellipse(self.screen, (150, 200, 255), (50 + i * 250, 120, 200, 100))
        
        # Draw control panel
        pygame.draw.rect(self.screen, (50, 50, 50), (0, 400, self.game.SCREEN_WIDTH, 100))
        for i in range(5):
            pygame.draw.circle(self.screen, (255, 0, 0), (100 + i * 150, 450), 20)

    def draw_characters(self):
        """
        Draw the characters in the spaceship.
        """
        for i, character in enumerate(self.characters):
            # Draw character "seat"
            pygame.draw.rect(self.screen, (70, 70, 70), (50 + i * 180, 300, 150, 200))
            
            # Draw character
            character.rect.topleft = (75 + i * 180, 325)
            self.screen.blit(character.image, character.rect.topleft)

    def draw_current_dialogue(self):
        """
        Draw the current dialogue for the speaking character.
        """
        if self.current_segment < len(self.inside_ship_segments):
            segment = self.inside_ship_segments[self.current_segment]
            speaker, text = segment["text"].split(": ", 1)
            
            # Find the speaking character's index
            speaker_index = next(i for i, char in enumerate(self.characters) if char.name == speaker)
            
            # Draw the text bubble
            self.draw_text_bubble(text, 50 + speaker_index * 180, 200)

    def draw_text_bubble(self, text, x, y):
        """
        Draw a text bubble with the given text.
        Args:
            text (str): The text to display in the bubble
            x (int): The x-coordinate of the bubble
            y (int): The y-coordinate of the bubble
        """
        wrapped_text = textwrap.fill(text, width=20)
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in wrapped_text.split('\n')]
        
        # Calculate bubble size
        bubble_width = max(surface.get_width() for surface in text_surfaces) + 20
        bubble_height = sum(surface.get_height() for surface in text_surfaces) + 20
        
        # Draw bubble
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, bubble_width, bubble_height), 2, border_radius=10)
        
        # Draw text
        y_offset = 10
        for surface in text_surfaces:
            self.screen.blit(surface, (x + 10, y + y_offset))
            y_offset += surface.get_height()

    def draw_story_segment(self):
        """
        Draw the current story segment.
        """
        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[self.current_segment]
            text = segment["text"]
            position = segment["position"]

            # Wrap the text
            wrapped_text = textwrap.fill(text, width=60)  # might need to adjust width

            # Render the wrapped text
            text_lines = wrapped_text.split("\n")
            text_surfaces = [
                self.font.render(line, True, (255, 255, 255)) for line in text_lines
            ]

            # Calculate the text box size based on wrapped text
            text_box_width = max([text_surface.get_width() for text_surface in text_surfaces]) + 20
            text_box_height = sum([text_surface.get_height() for text_surface in text_surfaces]) + 20

            # Draw the text box with fade in/out effect
            alpha = int(self.fade_timer / self.fade_duration * 255)
            text_box_surface = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
            text_box_surface.fill((0, 0, 0, alpha))
            self.screen.blit(text_box_surface, position)

            # Draw the wrapped text with fade effect
            y_offset = 0
            for line in text_lines:
                text_surface = self.font.render(line, True, (255, 255, 255))
                text_surface.set_alpha(alpha)
                x_pos = int(position[0]) + 10
                y_pos = int(position[1]) + 10 + y_offset
                self.screen.blit(text_surface, (x_pos, y_pos))
                y_offset += text_surface.get_height()

    def on_resume(self):
        """
        Resume the story screen.
        """
        self.initialize_music()
