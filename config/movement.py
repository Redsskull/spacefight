"""Movement-related configuration settings"""

MOVEMENT_SETTINGS = {
    "base_speed": 200,
    "run_multiplier": 1.5,
    "jump_force": 400,
    "gravity": 800,
}

LEVEL_BOUNDS = {
    "left": 0,
    "right": 1280,
    "top": 0,
    "bottom": 720,
}

CHARACTER_BOUNDARIES = {
    "margin": 50,  # Keep character this far from screen edges
    "ground_height": 150,  # Height from bottom where characters stand
}
