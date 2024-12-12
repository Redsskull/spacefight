"""Enemy spawning configuration"""

# Spawn points and timing
ENEMY_SPAWN = {
    "max_enemies": 10,
    "spawn_cooldown": 3.0,
    "spawn_points": [
        (-50, 447),
        (-50, 500),
        (-50, 575),
        (1250, 447),
        (1250, 500),
        (1250, 575),
    ],
    "wave_settings": {"enemies_per_wave": 5, "wave_cooldown": 10.0},
}
