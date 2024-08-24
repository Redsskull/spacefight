import pygame
from game import Game
from screen import MainMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


def main():
    """
    Main function of SpaceFight, the game.
    """
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.start()

if __name__ == "__main__":
    main()
