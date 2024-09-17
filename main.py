import pygame
from game import Game
from screens.main_menu import MainMenu

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#TODD: Add a user chice for game resolution


def main():
    """
    Main function of SpaceFight, the game.
    """
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.start()

if __name__ == "__main__":
    main()
