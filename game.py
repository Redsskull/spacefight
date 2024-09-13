import pygame
from screens import Screen, MainMenu


class Game:
    """
            Main game class that handle the game loop, screen changes and initialization
    """
    def __init__(self,screen_width, screen_height):
        """
            initializing the game.

            Args:
                screen_width (int): The width of the screen.
                screen_height (int): The height of the screen.
         """
        pygame.init()
        pygame.mixer.init()
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("SpaceFight")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = None
        self.main_menu = MainMenu(self) #I think I need this here..

    def start(self):
        """
            Start the game by setting the current screen to MainMenu and run the game loop.
        """
        self.current_screen = MainMenu(self)
        self.run()

    def run(self):
        """
            The main game loop that handle events, update and draw the screen.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_events(self):
        """
            Handle game events. including quitting.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        if self.current_screen:
            self.current_screen.handle_events(events)

    def update(self):
        """
            Update the current screen.
        """
        if self.current_screen:
            self.current_screen.update()

    def draw(self):
        """
            Draw the current screen if it exists.
        """
        if self.current_screen:
            self.current_screen.draw()

    def change_screen(self, new_screen):
        """
            Change the current screen to the new screen.

            Args:
                new_screen (Screen): The new screen to change to.
        """
        self.current_screen = new_screen
