import pygame
from screen import MainMenu


class Game:
    def __init__(self,screen_width, screen_height):
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("SpaceFight")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = None

    def start(self):
        self.current_screen = MainMenu(self)
        self.run()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self):
        if self.current_screen:
            self.current_screen.draw()

    def change_screen(self, new_screen):
        self.current_screen = new_screen
