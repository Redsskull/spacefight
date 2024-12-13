"""Animation management system"""

from typing import Dict, Optional, Tuple
import pygame
import logging
from graphics.animator import Animator
from graphics.effects import VisualEffects
from config.graphics import ANIMATION_SETTINGS, SPRITE_SETTINGS
from config.characters import CHARACTER_SPRITES


class AnimationManager:
    """Manages animation states and transitions for game entities"""

    def __init__(self):
        """Initialize the animation manager"""
        self.animators: Dict[int, Animator] = {}  # Map entity ID to its animator
        self.effects: Dict[int, VisualEffects] = {}  # Map entity ID to its effects
        self.sprite_sheets: Dict[int, Dict] = {}  # Entity sprite sheets
        self.entity_configs: Dict[int, Dict] = {}  # Entity-specific configs

    def register_entity(self, entity_id: int, sprite_config: Dict = None) -> None:
        """
        Register a new entity for animation management

        Args:
            entity_id (int): Unique identifier for the entity
            sprite_config (Dict): Entity-specific sprite configuration
        """
        self.animators[entity_id] = Animator()
        self.effects[entity_id] = VisualEffects()
        if sprite_config:
            self.entity_configs[entity_id] = sprite_config

    def load_sprite_sheets(self, entity_id: int, name: str, sprite_path: str) -> bool:
        """
        Load sprite sheets for an entity

        Args:
            entity_id (int): Entity identifier
            name (str): Entity name (e.g. "Regar", "Susan")
            sprite_path (str): Path to sprite directory

        Returns:
            bool: True if sprites loaded successfully
        """
        if name not in CHARACTER_SPRITES:
            logging.error(f"No sprite configuration found for {name}")
            return False

        try:
            sprite_sheets = {}
            for anim_type, info in CHARACTER_SPRITES[name].items():
                sprite_name = info["name"]
                full_path = f"{sprite_path}/{sprite_name}.png"

                try:
                    original_surface = pygame.image.load(full_path).convert_alpha()
                    scaled_surface = self._scale_sprite(
                        original_surface, name, self.entity_configs.get(entity_id, {})
                    )
                    sprite_sheets[anim_type] = {
                        "surface": scaled_surface,
                        "frames": info["frames"],
                    }
                except pygame.error as e:
                    logging.error(f"Failed to load {sprite_name}.png: {e}")
                    continue

            self.sprite_sheets[entity_id] = sprite_sheets
            return True

        except Exception as e:
            logging.error(f"Failed to load sprites for {name}: {e}")
            return False

    def _scale_sprite(
        self, surface: pygame.Surface, entity_name: str, entity_config: Dict
    ) -> pygame.Surface:
        """Scale sprite based on configuration"""
        target_height = SPRITE_SETTINGS["TARGET_HEIGHT"]
        scale_factor = entity_config.get("scale_factor", 1.0)

        # Calculate scaling
        base_scale = target_height / surface.get_height()
        final_scale = base_scale * scale_factor

        scaled_width = int(surface.get_width() * final_scale)
        scaled_height = int(target_height * scale_factor)

        return pygame.transform.scale(surface, (scaled_width, scaled_height))

    def update_animation(
        self, entity_id: int, dt: float, should_flip: bool
    ) -> Optional[pygame.Surface]:
        """
        Update animation state for an entity

        Args:
            entity_id (int): Entity identifier
            dt (float): Time delta since last update
            should_flip (bool): Whether sprites should be flipped

        Returns:
            Optional[pygame.Surface]: Current animation frame if available
        """
        if entity_id not in self.animators or entity_id not in self.sprite_sheets:
            return None

        return self.animators[entity_id].update(
            dt, self.sprite_sheets[entity_id], should_flip
        )

    def set_animation(self, entity_id: int, animation_name: str) -> None:
        """Set current animation for an entity"""
        if entity_id in self.animators:
            self.animators[entity_id].current_animation = animation_name

    def update_effects(self, entity_id: int, dt: float, sprite: pygame.Surface) -> bool:
        """Update visual effects for an entity"""
        if entity_id not in self.effects:
            return False
        return self.effects[entity_id].update_death_effect(dt, sprite)

    def set_dying(self, entity_id: int, is_dying: bool) -> None:
        """Set dying state for an entity"""
        if entity_id in self.effects:
            self.effects[entity_id].is_dying = is_dying

    def set_hurt(self, entity_id: int, is_hurt: bool) -> None:
        """Set hurt state for an entity"""
        if entity_id in self.effects:
            self.effects[entity_id].is_hurt = is_hurt

    def get_sprite_dimensions(self, entity_id: int) -> Optional[Tuple[int, int]]:
        """Get current sprite dimensions for collision updates"""
        if entity_id not in self.sprite_sheets:
            return None

        first_sheet = next(iter(self.sprite_sheets[entity_id].values()))
        surface = first_sheet["surface"]
        frames = first_sheet["frames"]

        width = surface.get_width() // frames
        height = surface.get_height()
        return (width, height)

    def is_animation_complete(self, entity_id: int) -> bool:
        """Check if entity's current animation is complete"""
        if entity_id in self.effects:
            return self.effects[entity_id].animation_complete
        return False

    def reset(self) -> None:
        """Reset all animation states"""
        self.animators.clear()
        self.effects.clear()
        self.sprite_sheets.clear()
        self.entity_configs.clear()

    def queue_animation(self, entity_id: int, animation_name: str, priority: int = 0):
        """Queue an animation with priority"""
        if entity_id in self.animators:
            self.animators[entity_id].queue_animation(animation_name, priority)

    def add_particle_effect(
        self, entity_id: int, position: Tuple[float, float], color: Tuple[int, int, int]
    ):
        """Add particle effect for an entity"""
        if entity_id in self.effects:
            self.effects[entity_id].add_particle_effect(position, color)

    def handle_impact(self, entity_id: int, position: Tuple[float, float]):
        """Handle impact effect for an entity"""
        if entity_id in self.effects:
            self.effects[entity_id].handle_impact_effect(position)

    def update_particles(self, entity_id: int, dt: float, surface: pygame.Surface):
        """Update particle effects for an entity"""
        if entity_id in self.effects:
            self.effects[entity_id].update_particles(dt, surface)

    def interrupt_animation(self, entity_id: int):
        """Interrupt current animation"""
        pass
