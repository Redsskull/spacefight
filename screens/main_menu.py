import pygame
from .base import Screen
from managers.sound_manager import SoundManager 

class MainMenu(Screen):
    """
    The main menu screen. Allows the player to start the game, open options, or quit.
    """

    def __init__(self, game):
        """
        Initialize the main menu screen.
        Args:
            game (Game): The game object
        """
        super().__init__(game)
        self.background = pygame.image.load("assets/art/main_menu_background.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )

        self.font = pygame.font.Font(None, 36)
        self.title = self.font.render("SpaceFight", True, (255, 255, 255))
        self.title_rect = self.title.get_rect(center=(self.game.SCREEN_WIDTH // 2, 100))

        self.menu_items = ["Start", "Options", "Quit"]
        self.menu_rects = []
        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, (255, 255, 255))
            rect = text.get_rect(center=(self.game.SCREEN_WIDTH // 2, 300 + i * 50))
            self.menu_rects.append((text, rect))

        # Initialize sound manager
        self.sound_manager = SoundManager()
        self.main_menu_music = "assets/sound/main_menu.mp3"

        # Track the currently selected menu item
        self.selected_index = 0

    def initialize_music(self):
        """
        Initialize the music for the main menu screen using SoundManager.
        """
        self.sound_manager.load_music("assets/sound/main_menu.mp3")
        self.sound_manager.play_music(-1)

    def handle_events(self, events):
        """
        Handle events for the main menu screen.
        Args:
            events (List[Event]): A list of pygame events
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, (_, rect) in enumerate(self.menu_rects):
                        if rect.collidepoint(event.pos):
                            self.selected_index = i
                            self.select_menu_item()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    self.select_menu_item()

    def select_menu_item(self):
        """
        Perform the action associated with the currently selected menu item.
        """
        if self.selected_index == 0:  # Start
            self.sound_manager.stop_music()
            from .story_screen import StoryScreen  # Import here to avoid circular import
            self.game.change_screen(StoryScreen(self.game))
        elif self.selected_index == 1:  # Options
            print("Open options")  # Replace with options screen logic
        elif self.selected_index == 2:  # Quit
            self.sound_manager.stop_music()
            self.game.running = False

    def draw(self):
        """
        Draw the main menu screen.
        """
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, self.title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Track the mouse and the selection
        for i, (text, rect) in enumerate(self.menu_rects):
            color = (255, 255, 255)
            if rect.collidepoint(mouse_pos):
                self.selected_index = i
                break

        for i, (text, rect) in enumerate(self.menu_rects):
            color = (255, 255, 255)  # Default color
            if i == self.selected_index:
                color = (0, 255, 0)  # Selected color

            text = self.font.render(self.menu_items[i], True, color)
            self.screen.blit(text, rect)

    def on_resume(self):
        """
        Resume the main menu screen.
        """
        # Check if current music is not the main menu music
        if pygame.mixer.music.get_busy() and pygame.mixer.music.get_pos() > 0:
            current_music = pygame.mixer.music.get_pos()
            if current_music != self.main_menu_music:
                self.initialize_music()
            else:
                self.initialize_music()
