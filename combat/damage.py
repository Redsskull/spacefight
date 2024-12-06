from typing import Dict, Any
from config import CHARACTER_STATS, SPECIAL_ATTACK_SETTINGS


class DamageSystem:
    """Handles damage calculations and modifications"""

    def __init__(self):
        self.modifiers: Dict[str, float] = {}

    def calculate_damage(
        self, base_damage: int, attacker_type: str, defender_type: str
    ) -> int:
        """Calculate final damage after applying modifiers"""
        final_damage = base_damage

        # Apply any type-specific modifiers
        if attacker_type in self.modifiers:
            final_damage *= self.modifiers[attacker_type]

        # Special attack bonus damage
        if attacker_type in SPECIAL_ATTACK_SETTINGS:
            special_config = SPECIAL_ATTACK_SETTINGS[attacker_type]
            if "damage" in special_config:
                final_damage = special_config["damage"]

        return int(final_damage)

    def register_modifier(self, entity_type: str, modifier: float) -> None:
        """Register a damage modifier for an entity type"""
        self.modifiers[entity_type] = modifier
