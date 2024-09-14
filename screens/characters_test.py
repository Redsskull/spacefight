import pygame
from .base import Screen
from characters import Regar, Susan, Emily, Bart


class CharacterTest(Screen):
    """
    temporary screen to test character animations
    """

    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.Surface(
            (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )
        self.background.fill((0, 0, 0))

        # character instances
        self.regar = Regar()
        self.susan = Susan()
        self.emily = Emily()
        self.bart = Bart()

        # character positions
        self.regar.position = pygame.math.Vector2(100, 100)
        self.susan.position = pygame.math.Vector2(200, 100)
        self.emily.position = pygame.math.Vector2(300, 100)
        self.bart.position = pygame.math.Vector2(400, 100)

        # Grooup all characters
        self.all_characters = pygame.sprite.Group()
        self.all_characters.add(self.regar, self.susan, self.emily, self.bart)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_screen(self.game.main_menu)
                    self.game.main_menu.on_resume()

    def update(self):
        dt = self.game.clock.tick(60) / 1000.0  # trying delta time
        self.all_characters.update(dt)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_characters.draw(self.screen)
