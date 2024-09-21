import pygame
import textwrap
from .base import Screen
from characters import Regar, Susan, Emily, Bart
import random

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
        self.background = pygame.image.load("assets/deep_space.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )

        self.font = pygame.font.Font(None, 36)

        # Define story segments with positions
        self.intro_segments = [
            {
                "text": "In the vast expanse of deep space, the mining vessel 'Hyperion' drifts silently, its hull scarred by two years of relentless cosmic wear.",
                "position": (50, 50),
            },
            {
                "text": "Inside, the skeleton crew of four carries the weight of isolation and the yearning for home.",
                "position": (350, 150),
            },
            {
                "text": "Captain Regar stands at the helm, his weathered face a testament to countless decisions that have kept them alive.",
                "position": (50, 250),
            },
            {
                "text": "As they approach the final leg of their journey, an unexpected signal breaks the monotony of space...",
                "position": (350, 350),
            },
            {"text": "Little do they know, their greatest adventure is about to begin!", "position": (50, 450)},
        ]

        self.inside_ship_segments = [
            {"text": "Regar: Alright people, we've got an unidentified signal. This close to home, I'm not taking any chances. Status report!"},
            {"text": "Susan: Analyzing the signal now, Captain. It doesn't match any known patterns in our database."},
            {"text": "Bart: Hey Em, want to check out this 'signal' in the observatory later? I hear the view is... stellar."},
            {"text": "Emily: In your dreams, flyboy. But speaking of dreams, the engines are operating beyond expected parameters. We might just get home early."},
            {"text": "Regar: Focus, people. Susan, any theories on that signal?"},
            {"text": "Susan: It could be a distress call, or... something else entirely. Logic suggests we proceed with caution."},
            {"text": "Bart: Or it could be a party invitation! Two years out here, I'd kill for a good party."},
            {"text": "Emily: The only thing you're killing is my concentration, Bart. But... I wouldn't mind a little celebration when we crack this mystery."},
            {"text": "Regar: Steady on, crew. Whatever's out there, we face it together. Just like we have for the past two years. Prepare for potential contact."}
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
        self.screen.fill((50, 50, 70))  # Darker, cooler grey for a more atmospheric feel
        
        # Draw windows showing deep space
        for i in range(3):
            pygame.draw.ellipse(self.screen, (10, 10, 40), (50 + i * (self.game.SCREEN_WIDTH // 3), 50, 200, 100))
            # Add some stars
            for _ in range(20):
                x = 50 + i * (self.game.SCREEN_WIDTH // 3) + random.randint(0, 200)
                y = 50 + random.randint(0, 100)
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Draw control panel with more details
        panel_width = self.game.SCREEN_WIDTH - 100
        pygame.draw.rect(self.screen, (70, 70, 80), (50, self.game.SCREEN_HEIGHT - 120, panel_width, 80))
        for i in range(5):
            pygame.draw.circle(self.screen, (200, 50, 50), (100 + i * (panel_width // 5), self.game.SCREEN_HEIGHT - 80), 15)
            pygame.draw.circle(self.screen, (50, 200, 50), (130 + i * (panel_width // 5), self.game.SCREEN_HEIGHT - 100), 10)

        # Draw character "stations" instead of seats
        station_width = (self.game.SCREEN_WIDTH - 150) // 4
        for i in range(4):
            pygame.draw.rect(self.screen, (60, 60, 80), (50 + i * (station_width + 25), 250, station_width, 200))
            # Add some details to each station
            pygame.draw.rect(self.screen, (80, 80, 100), (60 + i * (station_width + 25), 260, station_width - 20, 50))

    def draw_characters(self):
        """
        Draw the characters in the spaceship.
        """
        station_width = (self.game.SCREEN_WIDTH - 150) // 4
        for i, character in enumerate(self.characters):
            # Calculate character position
            x = 75 + i * (station_width + 25)
            y = 300
            
            # Draw character
            character.rect.topleft = (x, y)
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
            
            # Calculate bubble position
            station_width = (self.game.SCREEN_WIDTH - 150) // 4
            x = 75 + speaker_index * (station_width + 25)
            y = 200
            
            # Draw the text bubble
            self.draw_text_bubble(text, x, y)

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
        pygame.draw.rect(self.screen, (200, 200, 220), (x, y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 120), (x, y, bubble_width, bubble_height), 2, border_radius=10)
        
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
