from .base import BaseCharacter
from .traits.movement import MovementMixin
from .traits.combat import CombatMixin
from .traits.animations import AnimationMixin


class Character(BaseCharacter, MovementMixin, CombatMixin, AnimationMixin):
    """Base class combining all character functionality"""

    def __init__(self, name: str, game: "Game"):
        BaseCharacter.__init__(self, name, game)
        MovementMixin.__init__(self)
        CombatMixin.__init__(self)
        AnimationMixin.__init__(self)


class Regar(Character):
    def __init__(self, game):
        super().__init__("Regar", game)
        self.ranged_attacker = True
        self.has_special_attack = True


class Susan(Character):
    def __init__(self, game):
        super().__init__("Susan", game)
        self.has_special_attack = False


class Emily(Character):
    def __init__(self, game):
        super().__init__("Emily", game)
        self.has_special_attack = True


class Bart(Character):
    def __init__(self, game):
        super().__init__("Bart", game)
        self.base_facing_left = True
