import pygame
from .base import Screen

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
        self.background = pygame.image.load("assets/main_menu_background.png").convert()
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

        # Load and play the background music
        pygame.mixer.music.load("assets/main_menu.mp3")
        pygame.mixer.music.play(-1)

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
                            if i == 0:  # Start
                                print(
                                    "Start game"
                                )  # Replace with actual game start logic
                            elif i == 1:  # Options
                                print(
                                    "Open options"
                                )  # Replace with options screen logic
                            elif i == 2:  # Quit
                                pygame.mixer.music.stop()
                                self.game.running = False

    def draw(self):
        """
        Draw the main menu screen.

        """
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, self.title_rect)
        for text, rect in self.menu_rects:
            self.screen.blit(text, rect)

