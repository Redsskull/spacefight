import pygame
from .base import Screen
from .story_screen import StoryScreen


class CharacterSelector(Screen):
    """
    Screen for selecting characters for a 2-player game
            Args:
                Sxcreen (Screen): Base class for all screens
    """
    def __init__(self, game):
        """
        Initialize the character selector screen
                Args:
                    game (Game): The game instance
        """
        super().__init__(game)
        self.game = game
        self.initialize_sounds()
        self.story_screen = StoryScreen(self.game, init_sound=False) #TODO: When I have proper backgrounds, I don't need to import and intiliaze this at all. 


        self.player1_index = 0
        self.player2_index = 0
        self.player1_locked = False
        self.player2_locked = False
        self.player2_joined = False

        self.font = pygame.font.Font(None, 36)
        self.error_message = None
        self.error_timer = 0

    def initialize_sounds(self):
        """
        Initialize the sounds for the character selector screen
        I am using music stop here just to be sure

        """
        self.game.sound_manager.stop_music()
        self.game.sound_manager.load_music( "assets/sound/Choose_your_character.mp3")
        self.game.sound_manager.play_music(-1)
        self.game.sound_manager.load_sound("move", "assets/sound/punch.mp3")
        self.game.sound_manager.load_sound("lock", "assets/sound/metal_sound.mp3")

    def handle_events(self, events):
        """
        Handle events for the character selector screen
                Args:
                    events (Event): The events to handle
        Lots of keys for the players to push, or to identify when player 2 wants to play.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_a:
                    self.move_selection(-1, is_player1=True)
                elif event.key == pygame.K_d:
                    self.move_selection(1, is_player1=True)
                elif event.key == pygame.K_RETURN:
                    self.lock_character(is_player1=True)

                # Player 2 controls
                elif event.key == pygame.K_SPACE:
                    if not self.player2_joined:
                        self.player2_joined = True
                        self.player2_index = (self.player1_index + 1) % len(
                            self.game.character_manager.characters
                        )
                    else:
                        self.lock_character(is_player1=False)
                elif event.key == pygame.K_LEFT and self.player2_joined:
                    self.move_selection(-1, is_player1=False)
                elif event.key == pygame.K_RIGHT and self.player2_joined:
                    self.move_selection(1, is_player1=False)
                elif event.key == pygame.K_KP_ENTER and self.player2_joined:
                    self.lock_character(is_player1=False)

    def move_selection(self, direction, is_player1):
        """
        Move the character selection for a player
                Args:
                    direction (int): The direction to move the selection
                    is_player1 (bool): Whether the selection is for player 1
        logic here checks if the player is locked or not, and if the player is player 2, it checks if player 2 is joined or not.
        """
        if is_player1:
            if not self.player1_locked:
                self.player1_index = (self.player1_index + direction) % len(
                    self.game.character_manager.characters
                )
                self.game.sound_manager.play_sound("move")
        else:
            if self.player2_joined and not self.player2_locked:
                self.player2_index = (self.player2_index + direction) % len(
                    self.game.character_manager.characters
                )
                self.game.sound_manager.play_sound("move")

    def lock_character(self, is_player1):
        """
        Lock in the character selection for a player
                Args:
                    is_player1 (bool): Whether the selection is for player 1
        """
        if is_player1:
            self.player1_locked = True
            self.game.sound_manager.play_sound("lock")
        else:
            if self.player2_joined:
                self.player2_locked = True
                self.game.sound_manager.play_sound("lock")

        if self.player1_locked and (not self.player2_joined or self.player2_locked):
            self.start_game()

    def start_game(self):
        """
        Start the game with the selected characters
        """
        selected_indices = []

        if 0 <= self.player1_index < len(self.game.character_manager.characters):
            selected_indices.append(
                self.player1_index
            )
        else:
            self.show_error("Error: Invalid player 1 character index")
            return

        if self.player2_joined:
            if 0 <= self.player2_index < len(self.game.character_manager.characters):
                selected_indices.append(
                    self.player2_index
                )
            else:
                self.show_error("Error: Invalid player 2 character index")
                return

        if not selected_indices:
            self.show_error("Error: No characters selected")
            return

        print(f"Starting game with characters: {[self.game.character_manager.characters[i].name for i in selected_indices]}")
        self.game.sound_manager.stop_music()

        # Set the selected characters and start the game
        self.game.set_selected_characters(selected_indices)

        # Transition to the level screen
        from .level_screen import LevelScreen
        self.game.change_screen(LevelScreen(self.game))

    def show_error(self, message):
        """
        Show an error message on the screen
                Args:
                    message (str): The error message to show
        this method may change or be removed later. For now, i want to tell the player something has gone wrong.
        """
        self.error_message = message
        self.error_timer = 3000  # Show error for 3 seconds

    def update(self):
        """
        Update the character selector screen
        """
        if self.error_timer > 0:
            self.error_timer -= self.game.clock.get_time()
            if self.error_timer <= 0:
                self.error_message = None

    def draw(self):
        """
        Draw the character selector screen
        for now I am using the story screen to draw the background. I will change this later.
        when the game has its own art.
        """
        self.screen.fill((50, 50, 70))
        # Draw background
        self.story_screen.draw_spaceship_interior()

        # Draw characters
        self.game.character_manager.draw_characters(self.screen)

        # Draw selection boxes around Player 1 and Player 2's selected characters
        if 0 <= self.player1_index < len(self.game.character_manager.characters):
            player1_character = self.game.character_manager.characters[self.player1_index]
            pygame.draw.rect(
                self.screen, (0, 255, 0), player1_character.rect, 3
            )  # Green for Player 1

        if self.player2_joined and 0 <= self.player2_index < len(
            self.game.character_manager.characters
        ):
            player2_character = self.game.character_manager.characters[self.player2_index]
            pygame.draw.rect(
                self.screen, (255, 0, 0), player2_character.rect, 3
            )  # Red for Player 2

        self.draw_instructions()
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, (255, 0, 0))
            error_rect = error_surface.get_rect(
                center=(self.game.SCREEN_WIDTH // 2, self.game.SCREEN_HEIGHT - 50)
            )
            self.screen.blit(error_surface, error_rect)

    def draw_instructions(self):
        """
        Draw the instructions for the character selector screen
        """
        instructions = [
            "Player 1: A/D to move, Enter to select",
            "Player 2: Space to join, Left/Right to move, Space to select",
            (
                "Both players must select to start"
                if self.player2_joined
                else "Press Enter to start with one player"
            ),
        ]

        for i, instruction in enumerate(instructions):
            text_surface = self.font.render(instruction, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i * 30))
