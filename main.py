import sys
import logging
import pygame
from game import Game
from screens.main_menu import MainMenu
from config.graphics import SCREEN_WIDTH, SCREEN_HEIGHT

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Main function of SpaceFight, the game."""
    try:
        # Initialize Pygame
        if not pygame.init()[0]:
            raise pygame.error(f"Pygame failed to initialize: {pygame.get_error()}")

        logging.info("Starting SpaceFight...")
        game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)  # Use imported values
        game.start()

    except pygame.error as e:
        logging.error(f"Pygame error: {e}")
        return 1

    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        return 1

    finally:
        pygame.quit()
        logging.info("Game terminated")

    return 0


if __name__ == "__main__":
    sys.exit(main())

# I learned this when researching my game. exit codes may help if I ever work with other developers, so I parcticed here.
