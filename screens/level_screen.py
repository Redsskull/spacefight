import pygame
from .base import Screen


class LevelScreen(Screen):
    """
    This is the level one screen where the characters will battle enemies
    Args:
        Screen (Screen): Base class for all screens
    """
    def __init__(self, game):
        """
        Initialize the level one screen
        Args:
            game (Game): The game instance
        """
        super().__init__(game)
        self.game = game
        self.initialize_assets()
        self.initialize_sounds()
        self.initialize_characters()


    def initialize_assets(self):
        """
        Initialize the assets for the level one screen
        """
        self.background = pygame.image.load("assets/art/level_one.webp").convert()
        self.background = pygame.transform.scale(self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT))

    def initialize_sounds(self):
        """
        Initialize the sounds for the level one screen
        """
        self.game.sound_manager.stop_music()
        self.game.sound_manager.load_music("assets/sound/battlegamenoises.mp3")
        self.game.sound_manager.play_music(-1)

    def initialize_characters(self):
        """
        Initialize the players for the level one screen
        """
        selected_characters = self.game.get_selected_characters()
        self.game.character_manager.initialize_characters_for_level(selected_characters)


    def update(self):
        """
        Update the level one screen
        """
        dt = self.game.clock.get_time() / 1000 # Convert to seconds
        self.game.character_manager.update_characters(dt)

    def draw(self):
        """
        Draw the level one screen
        Args:
            screen (Surface): The surface to draw on
        """
        self.screen.blit(self.background, (0, 0))
        self.game.character_manager.draw_characters(self.screen)

    def handle_events(self, events):
        """
        Handle events for the level one screen
        Args:
            events (Event): The events to handle
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
