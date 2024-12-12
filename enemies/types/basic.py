"""Basic enemy type implementations"""

from ..base import BaseEnemy
from config.enemies import ENEMY_TYPES


class BasicEnemy(BaseEnemy):
    """Standard enemy type"""

    def __init__(self, game, spawn_position):
        super().__init__(game, spawn_position)
        self.stats = ENEMY_TYPES["basic"]


class FastEnemy(BaseEnemy):
    """Fast but weak enemy type"""

    def __init__(self, game, spawn_position):
        super().__init__(game, spawn_position)
        self.stats = ENEMY_TYPES["fast"]


class TankEnemy(BaseEnemy):
    """Slow but tough enemy type"""

    def __init__(self, game, spawn_position):
        super().__init__(game, spawn_position)
        self.stats = ENEMY_TYPES["tank"]
