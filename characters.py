"""
This module contains the character classes for the game. Each character has its own unique stats, abilities, and
visual representation. The base Character class provides the foundation for all characters, while the specific
character classes (e.g. Regar, Susan, Emily, Bart) define the unique properties for each character.
"""

import logging
from typing import Optional, Literal
import pygame
from game_states import GameState
from config import (
    CONTROLS,
    # Character related
    CHARACTER_STATS,
    CHARACTER_SPRITES,
    SPRITE_SETTINGS,
    REGAR_SPRITE_CONFIG,
    SUSAN_SPRITE_CONFIG,
    EMILY_SPRITE_CONFIG,
    # Combat related
    ATTACK_SETTINGS,
    SPECIAL_ATTACK_SETTINGS,
    # Animation related
    ANIMATION_SETTINGS,
)
from screens.level_screen import LevelScreen
from projectiles import EnergyShot


class Character(pygame.sprite.Sprite):
    """
    class for all characters in the game
    Args:
        pygame.sprite.Sprite: parent class
    """

    def __init__(self, name: str, game: "Game") -> None:
        """Initialize character
        Args:
            name: name of the character
            game: game instance
        """
        super().__init__()

        # Game and identity properties
        self.name = name
        self.game = game
        self.player_number = None

        # Character stats from config
        stats = CHARACTER_STATS[name]
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.speed = stats["speed"]
        self.strength = stats["strength"]
        self.color = stats["color"]

        # Position and movement properties
        self.position = pygame.math.Vector2()
        self.direction = pygame.math.Vector2()
        self.facing_right = True

        # Visual properties
        self.image = pygame.Surface((50, 100))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.visible = True

        # Sprite system properties
        self.using_sprites = False
        self.sprites_loaded = False
        self.sprite_sheets = {}
        self.available_animations = CHARACTER_SPRITES.get(self.name, {})

        # Animation properties
        self.current_animation = None
        self.animation_frame = 0
        self.frame_width = 0
        self.frame_height = 0
        self.animation_timer = 0
        self.animation_complete = False
        self.frame_duration = ANIMATION_SETTINGS["frame_duration"]

        # Combat properties - Basic Attack
        attack_settings = ATTACK_SETTINGS.get(self.name, ATTACK_SETTINGS["default"])
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = attack_settings["cooldown"]
        self.attack_range = pygame.Surface(attack_settings["range_size"])
        self.attack_range.fill(attack_settings["range_color"])
        self.attack_offset = attack_settings.get("offset", {"x": 0, "y": 0})

        # Combat properties - Special Attack
        self.has_special_attack = False
        self.is_special_attacking = False
        self.special_attack_timer = 0
        self.special_attack_cooldown = SPECIAL_ATTACK_SETTINGS["cooldown"]
        self.special_attack_animation_duration = ANIMATION_SETTINGS[
            "special_attack_duration"
        ]
        self.projectiles = pygame.sprite.Group()
        self.ranged_attacker = False

        # Death properties
        self.is_dying = False
        self.death_blink_duration = ANIMATION_SETTINGS["death"]["blink_duration"]
        self.death_blink_timer = self.death_blink_duration
        self.death_total_time = ANIMATION_SETTINGS["death"]["total_time"]
        self.blink_count = 0
        self.max_blinks = ANIMATION_SETTINGS["death"]["max_blinks"]

        # Debug properties
        self.direction_indicator = pygame.Surface((10, 10))
        self.direction_indicator.fill((0, 255, 0))

        # Initial sprite update
        self.update_sprite()

        # Hurt properties
        self.is_hurt = False
        self.hurt_timer = 0
        self.hurt_duration = ANIMATION_SETTINGS["frame_duration"]

    def take_damage(self, amount: int) -> None:
        """Take damage
        Args:
            amount: damage amount
        """
        self.health = max(0, self.health - amount)
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_blink_timer = self.death_blink_duration
            self.animation_complete = False
            self.blink_count = 0

        # Check if character has hurt animation available
        if self.using_sprites and not self.is_dying:
            if "hurt" in CHARACTER_SPRITES.get(self.name, {}):
                self.is_hurt = True
                self.hurt_timer = self.hurt_duration

    def update_sprite(self) -> None:
        """Updates the direction indicator for non-sprite characters"""
        if not self.using_sprites:  # Only update for non-sprite characters
            self.image.fill(self.color)
            if self.facing_right:
                self.image.blit(self.direction_indicator, (40, 45))
            else:
                self.image.blit(self.direction_indicator, (0, 45))

    def move(self, dt: float) -> None:
        """Move character
        Args:
            dt: time between frames
        """
        # Don't process movement if player number isn't set
        if self.player_number is None:
            return

        keys = pygame.key.get_pressed()
        player_controls = CONTROLS[f"player{self.player_number}"]["movement"]

        # Get directional input from configured keys
        self.direction.x = (
            keys[player_controls["right"]] - keys[player_controls["left"]]
        )
        self.direction.y = keys[player_controls["down"]] - keys[player_controls["up"]]

        # Update facing direction
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        movement = self.direction * self.speed * dt
        self.position += movement
        self.rect.topleft = int(self.position.x), int(self.position.y)

        self.update_sprite()

        if self.direction.length() > 0:
            print(f"{self.name} is moving to {self.position}")

    def attack(self, dt: float) -> None:
        """Handle character attacks
        Args:
            dt: time between frames
        return:
            None
        """
        if not self.game.is_in_state(GameState.LEVEL):
            return

        # Update attack timers
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.attacking = False

        # Update special attack cooldown
        if self.special_attack_timer > 0:
            self.special_attack_timer -= dt
            if self.special_attack_timer <= 0:
                self.is_special_attacking = False

        # Get player controls
        player_controls = CONTROLS[f"player{self.player_number}"]["combat"]

        # Handle player 1 (mouse controls)
        if self.player_number == 1:
            mouse = pygame.mouse.get_pressed()

            # Left click - normal attack
            if (
                mouse[player_controls["attack"] - 1]
                and not self.attacking
                and self.attack_timer <= 0
            ):
                self.attacking = True
                self.attack_timer = self.attack_cooldown
                if hasattr(self.game, "sound_manager"):
                    self.game.sound_manager.play_sound("punch")

            # Right click - special attack
            if (
                mouse[player_controls["special"] - 1]
                and not self.is_special_attacking
                and self.special_attack_timer <= 0
            ):
                if hasattr(self, "perform_special_attack"):
                    self.perform_special_attack()

        # Handle player 2 (keyboard controls)
        elif self.player_number == 2:
            keys = pygame.key.get_pressed()

            # Normal attack
            if (
                keys[player_controls["attack"]]
                and not self.attacking
                and self.attack_timer <= 0
            ):
                self.attacking = True
                self.attack_timer = self.attack_cooldown
                if hasattr(self.game, "sound_manager"):
                    self.game.sound_manager.play_sound("punch")

            # Special attack
            if (
                keys[player_controls["special"]]
                and not self.is_special_attacking
                and self.special_attack_timer <= 0
            ):
                if hasattr(self, "perform_special_attack"):
                    self.perform_special_attack()

        # Update projectiles and check collisions
        for projectile in list(self.projectiles):
            projectile.update(dt)
            for enemy in self.game.enemy_manager.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.take_damage(projectile.damage)
                    projectile.kill()
                    break

        # Handle melee attack collision
        if self.attacking:
            attack_rect = self.attack_range.get_rect()
            if hasattr(self, "sprite_config") and "attack_offset" in self.sprite_config:
                offset_x = self.sprite_config["attack_offset"]["x"]
                offset_y = self.sprite_config["attack_offset"]["y"]
                if self.facing_right:
                    attack_rect.midleft = (
                        self.rect.x + offset_x,
                        self.rect.y + offset_y,
                    )
                else:
                    attack_rect.midright = (
                        self.rect.right - offset_x,
                        self.rect.y + offset_y,
                    )
            else:
                # Default behavior
                if self.facing_right:
                    attack_rect.midleft = self.rect.midright
                else:
                    attack_rect.midright = self.rect.midleft

            # Check for collisions with enemies
            self.game.enemy_manager.handle_collision(attack_rect, self.strength)

    def load_sprite_sheets(self) -> None:
        """Load and configure sprite sheets for the character"""
        if self.name not in ["Regar", "Susan", "Emily"]:
            return

        try:
            sprite_path = f"assets/sprites/{self.name.lower()}"

            if self.name == "Susan":
                print(f"\nLoading {self.name} sprites from {sprite_path}")
                for anim_type, info in CHARACTER_SPRITES["Susan"].items():
                    sprite_name = info["name"]
                    full_path = f"{sprite_path}/{sprite_name}.png"
                    try:
                        original_surface = pygame.image.load(full_path).convert_alpha()
                        print(f"\n{anim_type} animation:")
                        print(
                            f"- Original dimensions: {original_surface.get_width()}x{original_surface.get_height()}"
                        )

                        # First scale to target height
                        base_height_scale = (
                            SUSAN_SPRITE_CONFIG["target_height"]
                            / original_surface.get_height()
                        )

                        # Then apply Susan's scale factor
                        final_scale = (
                            base_height_scale * SUSAN_SPRITE_CONFIG["scale_factor"]
                        )

                        scaled_width = int(original_surface.get_width() * final_scale)
                        scaled_height = int(
                            SUSAN_SPRITE_CONFIG["target_height"]
                            * SUSAN_SPRITE_CONFIG["scale_factor"]
                        )

                        scaled_surface = pygame.transform.scale(
                            original_surface, (scaled_width, scaled_height)
                        )
                        print(f"- Scaled dimensions: {scaled_width}x{scaled_height}")

                        self.sprite_sheets[anim_type] = {
                            "surface": scaled_surface,
                            "frames": info["frames"],
                        }

                        # Calculate frame width after scaling
                        frame_width = scaled_width // info["frames"]
                        self.rect.width = frame_width - (
                            SUSAN_SPRITE_CONFIG["collision_offset"]["x"] * 2
                        )
                        self.rect.height = scaled_height - (
                            SUSAN_SPRITE_CONFIG["collision_offset"]["y"] * 2
                        )
                        print(f"- Frame width: {frame_width}")
                        print(f"- Collision box: {self.rect.width}x{self.rect.height}")

                    except pygame.error as e:
                        print(f"Failed to load {sprite_name}.png: {e}")

                self.using_sprites = True
                self.sprites_loaded = True
                return

            if self.name == "Emily":
                print(f"\nLoading {self.name} sprites from {sprite_path}")
                for anim_type, info in CHARACTER_SPRITES["Emily"].items():
                    sprite_name = info["name"]
                    full_path = f"{sprite_path}/{sprite_name}.png"
                    # Add debug print for kick animation
                    if anim_type == "kick":
                        print("\nKick animation details:")
                        original_surface = pygame.image.load(full_path).convert_alpha()
                        print(
                            f"Original dimensions: {original_surface.get_width()}x{original_surface.get_height()}"
                        )
                    try:
                        original_surface = pygame.image.load(full_path).convert_alpha()
                        print(f"\n{anim_type} animation:")
                        print(
                            f"- Original dimensions: {original_surface.get_width()}x{original_surface.get_height()}"
                        )

                        # First scale to target height
                        base_height_scale = (
                            EMILY_SPRITE_CONFIG["target_height"]
                            / original_surface.get_height()
                        )

                        # Then apply Emily's scale factor
                        final_scale = (
                            base_height_scale * EMILY_SPRITE_CONFIG["scale_factor"]
                        )

                        scaled_width = int(original_surface.get_width() * final_scale)
                        scaled_height = int(
                            EMILY_SPRITE_CONFIG["target_height"]
                            * EMILY_SPRITE_CONFIG["scale_factor"]
                        )

                        scaled_surface = pygame.transform.scale(
                            original_surface, (scaled_width, scaled_height)
                        )
                        print(f"- Scaled dimensions: {scaled_width}x{scaled_height}")

                        self.sprite_sheets[anim_type] = {
                            "surface": scaled_surface,
                            "frames": info["frames"],
                        }

                        # Calculate frame width based on actual frames
                        frame_width = (
                            scaled_width // self.sprite_sheets[anim_type]["frames"]
                        )
                        print(f"- Frame width: {frame_width}")

                        # Update collision rect size with adjusted frame width
                        self.rect.width = frame_width - (
                            EMILY_SPRITE_CONFIG["collision_offset"]["x"] * 2
                        )
                        self.rect.height = scaled_height - (
                            EMILY_SPRITE_CONFIG["collision_offset"]["y"] * 2
                        )
                        print(f"- Collision box: {self.rect.width}x{self.rect.height}")

                    except pygame.error as e:
                        print(f"Failed to load {sprite_name}.png: {e}")

                self.using_sprites = True
                self.sprites_loaded = True
                return

            # Rest of existing Regar code unchanged
            # Get the first animation's dimensions to set base rect size
            first_anim = next(iter(CHARACTER_SPRITES["Regar"].items()))
            first_sheet = pygame.image.load(
                f"{sprite_path}/{first_anim[1]['name']}.png"
            ).convert_alpha()
            frame_height = SPRITE_SETTINGS["TARGET_HEIGHT"]
            frame_width = SPRITE_SETTINGS["TARGET_FRAME_WIDTH"]

            # Update rect size and position BEFORE loading other sprites
            current_bottom = self.rect.bottom  # Preserve the bottom position
            self.rect.width = frame_width - (
                REGAR_SPRITE_CONFIG["collision_offset"]["x"] * 2
            )
            self.rect.height = frame_height - (
                REGAR_SPRITE_CONFIG["collision_offset"]["y"] * 2
            )
            self.rect.bottom = current_bottom  # Maintain vertical position

            # Now load all sprite sheets
            for anim_type, info in CHARACTER_SPRITES["Regar"].items():
                sprite_name = info["name"]
                full_path = f"{sprite_path}/{sprite_name}.png"

                original_surface = pygame.image.load(full_path).convert_alpha()

                # Use original surface directly:
                scale_factor = (
                    SPRITE_SETTINGS["TARGET_HEIGHT"] / original_surface.get_height()
                )
                scale_factor *= REGAR_SPRITE_CONFIG["scale_factor"]

                scaled_surface = pygame.transform.scale(
                    original_surface,
                    (
                        int(original_surface.get_width() * scale_factor),
                        int(
                            SPRITE_SETTINGS["TARGET_HEIGHT"]
                            * REGAR_SPRITE_CONFIG["scale_factor"]
                        ),
                    ),
                )

                self.sprite_sheets[anim_type] = {
                    "surface": scaled_surface,
                    "frames": info["frames"],
                }

            self.using_sprites = True

            # Update collision rect with proper padding
            first_sheet = next(iter(self.sprite_sheets.values()))["surface"]
            first_frames = next(iter(self.sprite_sheets.values()))["frames"]
            self.frame_width = first_sheet.get_width() // first_frames
            self.frame_height = first_sheet.get_height()

            # Adjust collision rect with padding
            pad_x = REGAR_SPRITE_CONFIG["collision_offset"]["x"]
            pad_y = REGAR_SPRITE_CONFIG["collision_offset"]["y"]
            self.rect = pygame.Rect(
                self.rect.x + pad_x,
                self.rect.y + pad_y,
                self.frame_width - (pad_x * 2),
                self.frame_height - (pad_y * 2),
            )

        except (pygame.error, StopIteration) as e:
            logging.error(
                "Failed to load Regar sprites for animation '%s': %s",
                anim_type,
                e,
                exc_info=True,
            )
            self.using_sprites = False
        self.sprites_loaded = True

    def get_current_frame(self, animation_name: str) -> Optional[pygame.Surface]:
        """Get the current frame for the given animation
        Args:
            animation_name: name of the animation
        return:
            current frame
        """
        if animation_name not in self.sprite_sheets:
            return None

        sheet = self.sprite_sheets[animation_name]["surface"]
        frames = self.sprite_sheets[animation_name]["frames"]

        # Calculate frame width based on total sheet width and number of frames
        frame_width = sheet.get_width() // frames

        # Ensure animation frame stays within bounds
        current_frame = self.animation_frame % frames
        frame_x = current_frame * frame_width

        frame = sheet.subsurface((frame_x, 0, frame_width, sheet.get_height()))

        # Flip the frame horizontally if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        return frame

    def get_current_animation(
        self,
    ) -> Literal["idle", "walk", "attack", "shoot", "hurt", "kick"]:
        """
        Determine which animation to use based on state
        return:
            current animation
        """
        if self.is_hurt and "hurt" in CHARACTER_SPRITES.get(self.name, {}):
            return "hurt"
        if self.is_special_attacking:
            if self.ranged_attacker and "shoot" in self.sprite_sheets:
                return "shoot"
            elif "kick" in self.sprite_sheets:  # Emily's kick
                return "kick"
        elif self.attacking:
            return "attack"
        elif self.direction.length() > 0 and "walk" in self.sprite_sheets:
            return "walk"

        return "idle" if "idle" in self.sprite_sheets else "walk"

    def update(self, dt: float) -> None:
        """Update character and handle projectile collisions

        Args:
            dt: time between frames
        """
        if self.is_dying:
            self.death_total_time -= dt
            self.death_blink_timer -= dt
            if self.death_blink_timer <= 0:
                self.visible = not self.visible
                self.death_blink_timer = self.death_blink_duration
                if self.visible:
                    self.blink_count += 1

            if self.blink_count >= self.max_blinks or self.death_total_time <= 0:
                self.animation_complete = True
                self.visible = False
            return

        # Update projectiles and check collisions
        for projectile in self.projectiles:
            projectile.update(dt)
            # Check collision with enemies
            for enemy in self.game.enemy_manager.enemies:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.strength)
                    projectile.kill()
                    break

        if self.using_sprites:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                current_anim = self.get_current_animation()
                total_frames = self.sprite_sheets[current_anim]["frames"]
                self.animation_frame = (self.animation_frame + 1) % total_frames

                # Reset special attack when it's animation completes
                if (
                    self.is_special_attacking
                    or self.attacking
                    and self.animation_frame == total_frames - 1
                ):
                    self.is_special_attacking = False

            self.current_animation = self.get_current_animation()

        self.move(dt)
        self.attack(dt)

        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False

        if self.is_dying:
            # Blink effect using death_blink_speed
            current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
            if int(current_time / self.death_blink_speed) % 2 == 0:
                self.image.fill(self.color)
            else:
                self.image.fill((0, 0, 0))  # Blink to black

    def draw_debug_bounds(
        self,
        screen: pygame.Surface,
        frame_rect: pygame.Rect,
        attack_rect: Optional[pygame.Rect] = None,
    ) -> None:
        """Draw debug visualization for character bounds"""
        if SPRITE_SETTINGS["DEBUG_MODE"] and self.using_sprites:
            # Draw collision box in red
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

            # Draw sprite bounds in blue
            pygame.draw.rect(screen, (0, 0, 255), frame_rect, 2)

            # Calculate and draw attack range
            attack_config = ATTACK_SETTINGS.get(self.name, ATTACK_SETTINGS["default"])
            if "offset" in attack_config and self.attacking:
                offset_x = attack_config["offset"]["x"]
                offset_y = attack_config["offset"]["y"]

                # Draw attack range in magenta
                if attack_rect:
                    pygame.draw.rect(screen, (255, 0, 255), attack_rect, 2)

                # Draw attack origin point in yellow
                offset_point = (
                    (
                        self.rect.x + offset_x
                        if self.facing_right
                        else self.rect.right - offset_x
                    ),
                    self.rect.y + offset_y,
                )
                pygame.draw.circle(screen, (255, 255, 0), offset_point, 3)

    def draw(self, screen: pygame.Surface) -> None:
        self.projectiles.draw(screen)

        if self.is_dying and self.animation_complete:
            return

        if self.using_sprites and self.visible:
            current_frame = self.get_current_frame(self.current_animation)
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = self.rect.midbottom
                screen.blit(current_frame, frame_rect)

                # Draw attack range only when attacking
                if self.attacking:
                    attack_rect = self.attack_range.get_rect()
                    attack_config = ATTACK_SETTINGS.get(
                        self.name, ATTACK_SETTINGS["default"]
                    )
                    if "offset" in attack_config:
                        offset_x = attack_config["offset"]["x"]
                        offset_y = attack_config["offset"]["y"]

                        if self.facing_right:
                            attack_rect.midleft = (
                                self.rect.right,
                                self.rect.centery,
                            )
                        else:
                            attack_rect.midright = (
                                self.rect.left,
                                self.rect.centery,
                            )
                        screen.blit(self.attack_range, attack_rect)

                # Draw debug bounds always, outside attack condition
                self.draw_debug_bounds(
                    screen, frame_rect, attack_rect if self.attacking else None
                )
        else:
            # Non-sprite characters use same collision rect logic
            if self.visible:
                screen.blit(self.image, self.rect)
                if self.attacking:
                    attack_rect = self.attack_range.get_rect()
                    if self.facing_right:
                        attack_rect.midleft = self.rect.midright
                    else:
                        attack_rect.midright = self.rect.midleft
                    screen.blit(self.attack_range, attack_rect)

    def set_player_number(self, number: int) -> None:
        """
        sets player 1 or 2
        Args:
            number:number assigned to the player
        """
        self.player_number = number

    def perform_special_attack(self):
        """
        Base method that does nothing
        """
        # TODO: implament special attack for each character then make this an abstract method
        pass


class Regar(Character):
    """
    class for Regar character
    Args:
        Character: parent class
    """

    def __init__(self, game: "Game"):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Regar", game=game)
        self.ranged_attacker = True
        if isinstance(self.game.current_screen, LevelScreen):
            self.using_sprites = True
            self.load_sprite_sheets()
        self.has_special_attack = True

    def perform_special_attack(self):
        """
        method to perform special attack
        """
        if self.special_attack_timer <= 0:
            self.is_special_attacking = True  # Enable shoot animation
            self.animation_timer = 0  # Reset animation frame

            # Create projectile
            direction = (
                pygame.math.Vector2(1, 0)
                if self.facing_right
                else pygame.math.Vector2(-1, 0)
            )
            spawn_x = self.rect.right if self.facing_right else self.rect.left

            projectile = EnergyShot(
                pos=(spawn_x, self.rect.centery),
                direction=direction,
                damage=self.strength,
            )
            self.projectiles.add(projectile)

            # Set cooldown
            self.special_attack_timer = self.special_attack_cooldown

            # Play sound
            if hasattr(self.game, "sound_manager"):
                self.game.sound_manager.play_sound("shoot")


class Susan(Character):
    """
        class for Susan character
    Args:
        Character: parent class
    """

    def __init__(self, game):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Susan", game=game)
        if isinstance(self.game.current_screen, LevelScreen):
            self.using_sprites = True
            self.load_sprite_sheets()
        self.has_special_attack = False


class Emily(Character):
    """
        class for Emily character
    Args:
        Character: parent class
    """

    def __init__(self, game):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Emily", game=game)
        if isinstance(self.game.current_screen, LevelScreen):
            self.using_sprites = True
            self.load_sprite_sheets()
        self.has_special_attack = True  # Enable special attack
        self.kick_attack_range = pygame.Surface(
            (
                SPECIAL_ATTACK_SETTINGS["Emily"]["range"]["width"],
                SPECIAL_ATTACK_SETTINGS["Emily"]["range"]["height"],
            )
        )
        self.kick_attack_range.fill((255, 0, 0))  # Red for kick range

    def perform_special_attack(self):
        """Perform Emily's special kick attack"""
        if self.special_attack_timer <= 0:
            self.is_special_attacking = True
            self.animation_timer = 0
            self.special_attack_timer = SPECIAL_ATTACK_SETTINGS["Emily"]["cooldown"]

            # Create kick hitbox
            kick_rect = self.kick_attack_range.get_rect()
            offset_x = SPECIAL_ATTACK_SETTINGS["Emily"]["offset"]["x"]
            offset_y = SPECIAL_ATTACK_SETTINGS["Emily"]["offset"]["y"]

            if self.facing_right:
                kick_rect.midleft = (
                    self.rect.right + offset_x,
                    self.rect.centery + offset_y,
                )
            else:
                kick_rect.midright = (
                    self.rect.left - offset_x,
                    self.rect.centery + offset_y,
                )

            # Check for enemy hits
            for enemy in self.game.enemy_manager.enemies:
                if kick_rect.colliderect(enemy.rect):
                    enemy.take_damage(SPECIAL_ATTACK_SETTINGS["Emily"]["damage"])

            # Play sound effect
            if hasattr(self.game, "sound_manager"):
                self.game.sound_manager.play_sound("kick")


class Bart(Character):
    """
        class for Bart character
    Args:
        Character: parent class
    """

    def __init__(self, game):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Bart", game=game)
        self.update_sprite()
