import pygame
from .base import Screen
from managers.character_manager import CharacterManager
from .story_screen import StoryScreen
from .main_menu import MainMenu
from managers.sound_manager import SoundManager


class CharacterSelector(Screen):
    """
    CharacterSelector class
    Args:
        Screen (Screen): Screen class
    """

    def __init__(self, game):
        """
        Initialize CharacterSelector class
        Args:
            game (Game): Game class
        """
        super().__init__(game)
        self.game = game
        self.character_manager = CharacterManager(self.game)
        self.character_manager.initialize_characters()
        self.selected_characters = []
        self.max_players = 2
        self.font = pygame.font.Font(None, 36)
        self.story_screen = StoryScreen(self.game)

        #inititlize sound manager
        self.sound_manager = SoundManager()

    def handle_events(self, events):
        """
        Handle events based on user input
        Args:
            events (Event): Event class
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_character_selection(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if len(self.selected_characters) > 0:
                    self.start_game()

    def handle_character_selection(self, mouse_pos):
        """
        Handle character selection based on mouse position
        Args:
            mouse_pos (tuple): Mouse position
        """
        for i, character in enumerate(self.character_manager.characters):
            station_width = (self.game.SCREEN_WIDTH - 150) // 4
            x = 50 + i * (station_width + 25)
            y = 250
            if pygame.Rect(x, y, station_width, 200).collidepoint(mouse_pos):
                if character not in self.selected_characters:
                    if len(self.selected_characters) < self.max_players:
                        self.selected_characters.append(character)
                        self.sound_manager.play_sound("character_select")
                    else:
                        self.selected_characters.remove(character)


    def start_game(self):
        # TODO: Add start game logic, will print statemen and return to main menu for now
        print(
            f"stating game with characters: {[char.name for char in self.selected_characters]}"
        )
        self.sound_manager.stop_music()
        self.game.change_screen(MainMenu(self.game))

    def update(self):
        pass

    def draw(self):
        """
        This will draw the character selection screen
        """
        self.screen.fill((50, 50, 70))
        self.story_screen.draw_spaceship_interior()
        self.character_manager.draw_characters(self.screen)
        self.draw_selection_inditicators()
        self.draw_characters_names()
        self.draw_instructions()

    def draw_selection_inditicators(self):
        """
        Draw selection indicators
        """
        for character in self.selected_characters:
            if character in self.selected_characters:
                pygame.draw.rect(self.screen, (0, 255, 0), character.rect, 3)

    def draw_characters_names(self):
        """
        Draw characters names
        """
        for character in self.character_manager.characters:
            name_surface = self.font.render(character.name, True, (255, 255, 255))
            name_rect = name_surface.get_rect(
                center=(character.rect.centerx, character.rect.bottom + 20)
            )
            self.screen.blit(name_surface, name_rect)

    def draw_instructions(self):
        """
        An old Mortal Kombat like to choose your destinity(character)
        """

        instructions = [
            "Choose your destinty",
            f"Selected: {len(self.selected_characters)}/{self.max_players}",
            "Press Enter to start",
        ]

        for i, instruction in enumerate(instructions):
            text_surface = self.font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 30))
