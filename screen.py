import pygame


class Screen:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MainMenu(Screen):
    def __init__(self, game):
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
        pygame.mixer.music.load("assets/main_menu_music.wav")
        pygame.mixer.music.play(-1)

    def handle_events(self, events):
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
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, self.title_rect)
        for text, rect in self.menu_rects:
            self.screen.blit(text, rect)


# I will add more screens later on
