"""
This module contains the DamageSystem class, which handles damage calculations and modifications.
"""

from typing import Dict
from config import ANIMATION_SETTINGS


class DamageSystem:
    """Handles damage calculations and modifications"""

    def __init__(self):
        # Core damage properties
        self.modifiers: Dict[str, float] = {}

        # Death animation properties
        self.death_blink_duration = ANIMATION_SETTINGS["death"]["blink_duration"]
        self.death_total_time = ANIMATION_SETTINGS["death"]["total_time"]
        self.max_blinks = ANIMATION_SETTINGS["death"]["max_blinks"]

    def calculate_damage(
        self, base_damage: int, attacker_type: str, defender_type: str
    ) -> int:
        """Calculate final damage after applying modifiers"""
        final_damage = base_damage

        # Apply type-specific modifiers
        if attacker_type in self.modifiers:
            final_damage *= self.modifiers[attacker_type]

        return int(final_damage)

    def apply_damage(self, target: "Character", amount: int) -> None:
        """Apply damage to target and handle death/hurt states"""
        target.health = max(0, target.health - amount)

        # Check for death
        if target.health <= 0 and not target.is_dying:
            target.is_dying = True
            target.death_blink_timer = self.death_blink_duration
            target.animation_complete = False
            target.blink_count = 0

        # Handle hurt animation if available and not dying
        elif target.using_sprites and not target.is_dying:
            if "hurt" in target.sprite_sheets:
                target.is_hurt = True
                target.hurt_timer = ANIMATION_SETTINGS["frame_duration"]

    def register_modifier(self, entity_type: str, modifier: float) -> None:
        """Register a damage modifier for an entity type"""
        self.modifiers[entity_type] = modifier
