import pygame
import textwrap
import json
from .base import Screen
import random
from managers.character_manager import CharacterManager
from managers.sound_manager import SoundManager
from managers.screen_effects import ScreenEffectsManager

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
        self.game = game
        self.initialize_assets()
        self.initialize_managers()
        self.initialize_state()

    def initialize_assets(self):
        """
        Initialize the assets for the story screen.
        """
        self.background = pygame.image.load("assets/art/deep_space.png").convert()
        self.background = pygame.transform.scale(self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)

        # Load story from JSON file
        with open('assets/story.json', 'r') as f:
            self.story_data = json.load(f)

        # Start with the intro segments
        self.story_segments = self.story_data["intro"]

    def initialize_managers(self):
        """
        Initialize the managers for the story screen.
        """
        self.sound_manager = SoundManager()
        self.initialize_sounds()

        # Create character instances
        self.character_manager = CharacterManager(self.game)
        self.character_manager.initialize_characters()

        # Initialize screen effects manager
        self.screen_effects_manager = ScreenEffectsManager(self.screen, self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)

    def initialize_state(self):
        """
        Initialize the state variables for the story screen.
        """
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

    def initialize_sounds(self):
        """
        Initialize the sounds for the story screen using SoundManager.
        """
        self.sound_manager.load_music("assets/sound/battlegamenoises.mp3")
        self.sound_manager.play_music(-1)
        self.sound_manager.load_sound("alarm", "assets/sound/alarm.wav")

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
        dt = self.game.clock.get_time() / 1000

        # Update characters
        self.character_manager.update_characters(dt)
        self.character_manager.handle_character_movement(dt)
        self.character_manager.handle_character_attack()

        if self.current_segment < len(self.story_segments):
            # Fade in
            if self.fade_direction == 1:
                self.fade_timer += self.game.clock.get_time()
                if self.fade_timer >= self.fade_duration:
                    self.fade_direction = 0
                    self.fade_timer = self.fade_duration
            # Stay visible
            elif self.fade_direction == 0:
                if current_time - self.text_timer >= self.text_delay:
                    self.fade_direction = -1
                    self.fade_timer = self.fade_duration
            # Fade out
            elif self.fade_direction == -1:
                self.fade_timer -= self.game.clock.get_time()
                if self.fade_timer <= 0:
                    self.fade_direction = 1
                    self.fade_timer = 0
                    self.current_segment += 1
                    self.text_timer = current_time

        # Handle when all intro segments are done
        if self.current_segment >= len(self.story_segments):
            if self.state == "intro":
                # Transition to inside_ship state and load the new segments
                self.state = "inside_ship"
                self.story_segments = self.story_data["inside_ship"]  # Load from JSON
                self.current_segment = 0
            elif self.state == "inside_ship" and self.current_segment >= len(self.story_segments):
                from .main_menu import MainMenu  # Import here to avoid circular import
                self.game.change_screen(MainMenu(self.game))  # Return to main menu after the story

        # Trigger alarm and screen shake when proximity alarm is mentioned (segment 9 in inside_ship)
        if self.state == "inside_ship" and self.current_segment == 9:  # Adjust index as needed
            if not self.screen_effects_manager.shaking:
                self.sound_manager.play_sound("alarm")
                self.screen_effects_manager.start_shake(1000, 5)

        # Update screen shake logic
        self.screen_effects_manager.update()

    def draw(self):
        """
        Draw the story screen.
        """
        if self.state == "inside_ship":
            # Clear the screen with a solid color
            self.screen.fill((0, 0, 0))

            self.draw_spaceship_interior()
            self.character_manager.draw_characters(self.screen)
            self.draw_current_dialogue()

            # Draw Evil Bug Lord Sneaky's dialogue
            if self.current_segment == 12:  # Adjust index as needed
                self.draw_evil_bug_lord_dialogue()
        else:
            self.screen.blit(self.background, (0, 0))
            self.draw_story_segment()

        # Apply screen shake if active
        self.screen_effects_manager.apply_shake()

    def draw_spaceship_interior(self):
        """
        Draw the interior of the spaceship.
        """
        self.screen.fill((50, 50, 70))  # Darker, cooler grey for a more atmospheric feel

        # Draw windows showing deep space
        for i in range(3):
            pygame.draw.ellipse(self.screen, (10, 10, 40), (50 + i * (self.game.SCREEN_WIDTH // 3), 50, 200, 100))
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
            pygame.draw.rect(self.screen, (80, 80, 100), (60 + i * (station_width + 25), 260, station_width - 20, 50))

    def draw_current_dialogue(self):
        """
        Draw the current dialogue for the speaking character.
        """
        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[self.current_segment]
            speaker = segment.get("speaker", "")
            text = segment["text"]

            # Find the speaking character's index based on the speaker name
            speaking_character = self.character_manager.get_character_by_name(speaker)

            if speaking_character:
                # Calculate speaker position
                station_width = (self.game.SCREEN_WIDTH - 150) // 4
                speaker_index = self.character_manager.characters.index(speaking_character)
                speaker_x = 75 + speaker_index * (station_width + 25)
                speaker_y = 300

                # Draw the text bubble for the speaking character
                self.draw_text_bubble(text, speaker_x, speaker_y, speaker_x, speaker_y)

    def draw_text_bubble(self, text, speaker_x, speaker_y, bubble_x, bubble_y):
        """
        Draw a circular text bubble with an arrow coming out from it, pointing to the speaker.
        """
        wrapped_text = textwrap.fill(text, width=20)
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in wrapped_text.split('\n')]

        bubble_width = max(surface.get_width() for surface in text_surfaces) + 20
        bubble_height = sum(surface.get_height() for surface in text_surfaces) + 20
        bubble_radius = max(bubble_width, bubble_height) // 2 + 20

        # Adjust position based on speaker location, and prevent bubble from going off-screen
        if speaker_x < self.game.SCREEN_WIDTH // 2:
            bubble_x = min(speaker_x + 50, self.game.SCREEN_WIDTH - bubble_radius * 2)
        else:
            bubble_x = max(speaker_x - bubble_radius * 2 - 50, 0)

        bubble_y = max(speaker_y - bubble_radius - 50, 0)

        pygame.draw.ellipse(self.screen, (200, 200, 220), (bubble_x, bubble_y, bubble_radius * 2, bubble_radius * 2))
        pygame.draw.ellipse(self.screen, (100, 100, 120), (bubble_x, bubble_y, bubble_radius * 2, bubble_radius * 2), 2)

        arrow_start_x = bubble_x + bubble_radius if speaker_x < self.game.SCREEN_WIDTH // 2 else bubble_x + bubble_radius
        arrow_start_y = bubble_y + bubble_radius * 2
        pygame.draw.polygon(self.screen, (200, 200, 220), [
            (speaker_x, speaker_y),
            (arrow_start_x - 10, arrow_start_y),
            (arrow_start_x + 10, arrow_start_y)
        ])

        y_offset = bubble_radius - (bubble_height // 2) + 10
        for surface in text_surfaces:
            text_x = bubble_x + bubble_radius - (surface.get_width() // 2)
            self.screen.blit(surface, (text_x, bubble_y + y_offset))
            y_offset += surface.get_height()

    def draw_evil_bug_lord_dialogue(self):
        """
        Draw the dialogue for Evil Bug Lord Sneaky as a rectangular bubble on the left side of the screen.
        """
        text = "Greetings, humans of the Hyperion. Prepare to be assimilated into our glorious hive!"
        self.draw_rectangular_bubble(text, 20, 50)

    def draw_rectangular_bubble(self, text, x, y):
        """
        Draw a rectangular text bubble that grows to fit the text.
        """
        wrapped_text = textwrap.fill(text, width=40)
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in wrapped_text.split('\n')]

        bubble_width = max(surface.get_width() for surface in text_surfaces) + 20
        bubble_height = sum(surface.get_height() for surface in text_surfaces) + 20

        pygame.draw.rect(self.screen, (200, 200, 220), (x, y, bubble_width, bubble_height))
        pygame.draw.rect(self.screen, (100, 100, 120), (x, y, bubble_width, bubble_height), 2)

        y_offset = 10
        for surface in text_surfaces:
            text_x = x + 10
            self.screen.blit(surface, (text_x, y + y_offset))
            y_offset += surface.get_height() + 5

    def draw_story_segment(self):
        """
        Draw the current story segment.
        """
        if self.current_segment < len(self.story_segments):
            segment = self.story_segments[self.current_segment]
            text = segment["text"]
            position = segment["position"]

            wrapped_text = textwrap.fill(text, width=60)
            text_lines = wrapped_text.split("\n")
            text_surfaces = [self.font.render(line, True, (255, 255, 255)) for line in text_lines]

            text_box_width = max([text_surface.get_width() for text_surface in text_surfaces]) + 20
            text_box_height = sum([text_surface.get_height() for text_surface in text_surfaces]) + 20

            alpha = int(self.fade_timer / self.fade_duration * 255)
            text_box_surface = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
            text_box_surface.fill((0, 0, 0, alpha))
            self.screen.blit(text_box_surface, position)

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
        self.initialize_sounds()
