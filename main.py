import pygame
from game import Game
from screens.main_menu import MainMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def main():
    """
    Main function of SpaceFight, the game.
    """
    try:
        # Initialize Pygame
        if not pygame.init():
            raise pygame.error("Pygame failed to initialize.")
        
        # Initialize the game
        game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        game.start()
    
    except pygame.error as e:
        print(f"Pygame error: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    finally:
        # Ensure Pygame exits gracefully
        pygame.quit()

if __name__ == "__main__":
    main()
