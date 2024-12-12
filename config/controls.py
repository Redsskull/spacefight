"""Input control mappings"""

import pygame

CONTROLS = {
    "player1": {
        "movement": {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
        },
        "combat": {
            "attack": 1,  # Left mouse click
            "special": 3,  # Right mouse click
        },
    },
    "player2": {
        "movement": {
            "up": pygame.K_UP,
            "down": pygame.K_DOWN,
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
        },
        "combat": {
            "attack": pygame.K_SPACE,
            "special": pygame.K_RETURN,
        },
    },
}
