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
            {"text": "Regar: Steady on, crew. Whatever's out there, we face it together. Just like we have for the past two years. Prepare for potential contact."},
            {"text": "Susan: Captain! Proximity alarm triggered! Something's approaching fast!"},
            {"text": "Bart: Emily, if this is our last moment, I just want you to know... your hair looks fantastic even in a crisis."},
            {"text": "Emily: Bart, I swear, if we survive this, I'm going to-"},
            {"text": "Evil Bug Lord Sneaky: Greetings, humans of the Hyperion. Prepare to be assimilated into our glorious hive!"},
            {"text": "Regar: What in the blazes? Who are you? Crew, battle stations!"},
            {"text": "Susan: Captain, they're boarding the ship! Hostiles incoming!"},
            {"text": "Bart: Hey Em, how about we fight these bugs together? I promise I'm great at swatting!"},
            {"text": "Emily: This is hardly the time, Bart! But... stick close. We might need each other."},
            {"text": "Regar: All hands, prepare for combat! We're not going down without a fight!"}
        ]

        self.story_segments = self.intro_segments

        # Initialize sounds
        self.initialize_sounds()

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

        # Screen shake effect
        self.shake_duration = 1000  # 1 second of shaking
        self.shake_intensity = 5  # pixels
        self.shake_start_time = 0
        self.shaking = False

    def initialize_sounds(self):
        """
        Initialize the sounds for the story screen.
        """
        pygame.mixer.music.load("assets/battlegamenoises.mp3")
        pygame.mixer.music.play(-1)
        self.alarm_sound = pygame.mixer.Sound("assets/alarm.wav")

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
            elif self.state == "inside_ship" and self.current_segment >= len(self.inside_ship_segments):
                from .main_menu import MainMenu  # Import here to avoid circular import
                self.game.change_screen(MainMenu(self.game))  # Return to main menu after story

        # Trigger alarm and screen shake when proximity alarm is mentioned
        if self.state == "inside_ship" and self.current_segment == 9:  # Adjust index as needed
            if not self.shaking:
                self.alarm_sound.play()
                self.shake_start_time = current_time
                self.shaking = True

        # Update screen shake
        if self.shaking:
            if current_time - self.shake_start_time > self.shake_duration:
                self.shaking = False

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

            # Draw Evil Bug Lord Sneaky's dialogue
            if self.current_segment == 12:  # Adjust index as needed
                self.draw_evil_bug_lord_dialogue()
        else:
            self.screen.blit(self.background, (0, 0))
            self.draw_story_segment()

        # Apply screen shake if active
        if self.shaking:
            dx = random.randint(-self.shake_intensity, self.shake_intensity)
            dy = random.randint(-self.shake_intensity, self.shake_intensity)
            self.screen.blit(self.screen, (dx, dy))

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
            speaker_index = next((i for i, char in enumerate(self.characters) if char.name == speaker), None)
            
            if speaker_index is not None:
                # Calculate speaker position
                station_width = (self.game.SCREEN_WIDTH - 150) // 4
                speaker_x = 75 + speaker_index * (station_width + 25)
                speaker_y = 300
                
                # Draw the text bubble
                self.draw_text_bubble(text, speaker_x, speaker_y, speaker_x, speaker_y)

    def draw_evil_bug_lord_dialogue(self):
        """
        Draw the dialogue for Evil Bug Lord Sneaky as a rectangular bubble on the left side of the screen.
        """
        text = "Greetings, humans of the Hyperion. Prepare to be assimilated into our glorious hive!"
        self.draw_rectangular_bubble(text, 20, 50)

    def draw_rectangular_bubble(self, text, x, y):
        """
        Draw a rectangular text bubble that grows to fit the text.
        Args:
            text (str): The text to display in the bubble.
            x (int): The x-coordinate of the top-left corner of the bubble.
            y (int): The y-coordinate of the top-left corner of the bubble.
        """
        # Wrap and render the text
        wrapped_text = textwrap.fill(text, width=40)  # Adjust width for text wrapping
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in wrapped_text.split('\n')]

        # Dynamically calculate bubble width and height
        bubble_width = max(surface.get_width() for surface in text_surfaces) + 20  # 20 px padding
        bubble_height = sum(surface.get_height() for surface in text_surfaces) + 20  # 20 px padding

        # Draw the rectangle with the calculated dimensions
        pygame.draw.rect(self.screen, (200, 200, 220), (x, y, bubble_width, bubble_height))
        pygame.draw.rect(self.screen, (100, 100, 120), (x, y, bubble_width, bubble_height), 2)

        # Draw the text inside the bubble
        y_offset = 10
        for surface in text_surfaces:
            text_x = x + 10  # 10 px padding from the left
            self.screen.blit(surface, (text_x, y + y_offset))
            y_offset += surface.get_height() + 5  # Add line spacing

    def draw_text_bubble(self, text, speaker_x, speaker_y, bubble_x, bubble_y):
        """
        Draw a circular text bubble with an arrow coming out from it, pointing to the speaker.
        Args:
            text (str): The text to display in the bubble.
            speaker_x (int): The x-coordinate of the speaker.
            speaker_y (int): The y-coordinate of the speaker.
            bubble_x (int): The x-coordinate of the bubble.
            bubble_y (int): The y-coordinate of the bubble.
        """
        wrapped_text = textwrap.fill(text, width=20)
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in wrapped_text.split('\n')]
        
        bubble_width = max(surface.get_width() for surface in text_surfaces) + 20
        bubble_height = sum(surface.get_height() for surface in text_surfaces) + 20
        bubble_radius = max(bubble_width, bubble_height) // 2 + 20  # Circular bubble

        # Adjust position based on speaker location, and prevent bubble from going off-screen
        if speaker_x < self.game.SCREEN_WIDTH // 2:
            bubble_x = min(speaker_x + 50, self.game.SCREEN_WIDTH - bubble_radius * 2)  # Right of speaker
        else:
            bubble_x = max(speaker_x - bubble_radius * 2 - 50, 0)  # Left of speaker

        bubble_y = max(speaker_y - bubble_radius - 50, 0)  # Above the speaker, but not off-screen

        # Draw the bubble
        pygame.draw.ellipse(self.screen, (200, 200, 220), (bubble_x, bubble_y, bubble_radius * 2, bubble_radius * 2))
        pygame.draw.ellipse(self.screen, (100, 100, 120), (bubble_x, bubble_y, bubble_radius * 2, bubble_radius * 2), 2)

        # Draw the arrow pointing to the speaker
        arrow_start_x = bubble_x + bubble_radius if speaker_x < self.game.SCREEN_WIDTH // 2 else bubble_x + bubble_radius
        arrow_start_y = bubble_y + bubble_radius * 2
        pygame.draw.polygon(self.screen, (200, 200, 220), [
            (speaker_x, speaker_y),  # Tip of the arrow (at the speaker)
            (arrow_start_x - 10, arrow_start_y),  # Left base of the arrow
            (arrow_start_x + 10, arrow_start_y)  # Right base of the arrow
        ])

        # Draw the text
        y_offset = bubble_radius - (bubble_height // 2) + 10
        for surface in text_surfaces:
            text_x = bubble_x + bubble_radius - (surface.get_width() // 2)
            self.screen.blit(surface, (text_x, bubble_y + y_offset))
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
        self.initialize_sounds()
