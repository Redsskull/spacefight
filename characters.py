import pygame
from game_states import GameState
import logging
from typing import Optional, Tuple, List
from config import CHARACTER_STATS, ATTACK_SETTINGS, CHARACTER_SPRITES, SPRITE_SETTINGS, REGAR_SPRITE_CONFIG
import traceback
from screens.level_screen import LevelScreen


class Character(pygame.sprite.Sprite):
    """
    class for all characters in the game
    Args:
        pygame.sprite.Sprite: parent class
    """

    def __init__(self, name: str, game: "Game") -> None:
        """Initialize character"""
        super().__init__()
        
        # Basic attributes and stats
        self.name = name
        self.game = game
        stats = CHARACTER_STATS[name]
        self.health = stats["health"]
        self.speed = stats["speed"]
        self.strength = stats["strength"]
        self.color = stats["color"]

        # Attack properties
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = ATTACK_SETTINGS["cooldown"]
        self.attack_range = pygame.Surface(ATTACK_SETTINGS["range_size"])
        self.attack_range.fill(ATTACK_SETTINGS["range_color"])
        
        # Create surface and set color
        self.image = pygame.Surface((50, 100))
        self.image.fill(self.color)
        self.facing_right = True
        
        # Sprite initialization flags
        self.using_sprites = False
        self.sprites_loaded = False
        
        # Direction indicator
        self.direction_indicator = pygame.Surface((10, 10))
        self.direction_indicator.fill((0, 255, 0))
        
        # Position setup
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.player_number = None
        
        # Now safe to update sprite
        self.update_sprite()
        
        self.max_health = stats["health"]
        self.is_dying = False
        self.visible = True
        self.animation_complete = False
        self.blink_count = 0
        # Default timing values
        self.death_blink_duration = 0.2  # Time between blinks
        self.death_total_time = 2.0  # Total animation duration
        self.max_blinks = 10  # Number of blinks before death
        self.death_blink_timer = self.death_blink_duration

        # Initialize sprite sheets dict based on available animations
        self.sprite_sheets = {}
        self.available_animations = CHARACTER_SPRITES.get(self.name, {})
        self.ranged_attacker = "shoot" in self.available_animations

        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = 0.1  # Adjust timing as needed

    def take_damage(self, amount: int) -> None:
        """Take damage"""
        self.health = max(0, self.health - amount)
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_blink_timer = self.death_blink_duration
            self.animation_complete = False
            self.blink_count = 0

    def update_sprite(self):
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
        keys = pygame.key.get_pressed()
        if self.player_number == 1:
            self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
            self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        elif self.player_number == 2:
            self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]

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
        """Perform attack"""
        if not self.game.is_in_state(GameState.LEVEL):
            return
        
        # Get input based on player number
        if self.player_number == 1:
            mouse = pygame.mouse.get_pressed()
            is_attacking = mouse[0] or mouse[2]
        elif self.player_number == 2:
            keys = pygame.key.get_pressed()
            is_attacking = keys[pygame.K_RCTRL] or keys[pygame.K_RSHIFT]
        else:
            return

        # Handle attack initiation
        if is_attacking and not self.attacking and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            if hasattr(self.game, "sound_manager"):
                try:
                    self.game.sound_manager.play_sound("punch")
                except AttributeError:
                    logging.warning("Sound manager not available")

        # Handle attack collision and visuals
        if self.attacking:
            attack_rect = self.attack_range.get_rect()
            
            # Position attack from collision box (red rectangle)
            if self.facing_right:
                attack_rect.midleft = self.rect.midright
            else:
                attack_rect.midright = self.rect.midleft

            # Handle collision detection
            if self.game.is_in_state(GameState.LEVEL):
                if hasattr(self.game, "enemy_manager"):
                    self.game.enemy_manager.handle_collision(attack_rect, self.strength)

        # Update attack timer
        if self.attack_timer > 0:
            self.attack_timer -= dt
        else:
            self.attacking = False

    def load_sprite_sheets(self):
        """Load and configure sprite sheets for the character"""
        if self.name != "Regar":
            return
            
        try:
            sprite_path = f"assets/sprites/regar"
            
            # Get the first animation's dimensions to set base rect size
            first_anim = next(iter(CHARACTER_SPRITES["Regar"].items()))
            first_sheet = pygame.image.load(f"{sprite_path}/{first_anim[1]['name']}.png").convert_alpha()
            frame_height = SPRITE_SETTINGS["TARGET_HEIGHT"]
            frame_width = SPRITE_SETTINGS["TARGET_FRAME_WIDTH"]
            
            # Update rect size and position BEFORE loading other sprites
            current_bottom = self.rect.bottom  # Preserve the bottom position
            self.rect.width = frame_width - (REGAR_SPRITE_CONFIG["collision_offset"]["x"] * 2)
            self.rect.height = frame_height - (REGAR_SPRITE_CONFIG["collision_offset"]["y"] * 2)
            self.rect.bottom = current_bottom  # Maintain vertical position
            
            # Now load all sprite sheets
            for anim_type, info in CHARACTER_SPRITES["Regar"].items():
                # ... rest of your sprite loading code ...
                
                sprite_name = info["name"]
                full_path = f"{sprite_path}/{sprite_name}.png"
                
                original_surface = pygame.image.load(full_path).convert_alpha()
                
                # Use original surface directly:
                scale_factor = SPRITE_SETTINGS["TARGET_HEIGHT"] / original_surface.get_height() 
                scale_factor *= REGAR_SPRITE_CONFIG["scale_factor"]

                scaled_surface = pygame.transform.scale(
                    original_surface,
                    (int(original_surface.get_width() * scale_factor), 
                     int(SPRITE_SETTINGS["TARGET_HEIGHT"] * REGAR_SPRITE_CONFIG["scale_factor"]))
                )
                
                self.sprite_sheets[anim_type] = {
                    "surface": scaled_surface,
                    "frames": info["frames"]
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
                self.frame_height - (pad_y * 2)
            )

        except (pygame.error, StopIteration) as e:
            logging.error(f"Failed to load Regar sprites: {e}")
            self.using_sprites = False
        self.sprites_loaded = True

    def get_current_frame(self, animation_name):
        if (animation_name not in self.sprite_sheets):
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

    def get_current_animation(self):
        """Determine which animation to use based on state"""
        # Check sprite availability first
        if self.attacking:
            if self.ranged_attacker and "shoot" in self.sprite_sheets:
                return "shoot"
            if "attack" in self.sprite_sheets:
                return "attack"
        elif self.direction.length() > 0 and "walk" in self.sprite_sheets:
            return "walk"

        # Default to idle if available, otherwise walk
        return "idle" if "idle" in self.sprite_sheets else "walk"

    def update(self, dt):
        """
        method to update the character
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

        if self.using_sprites:
            self.animation_timer += dt
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                current_anim = self.get_current_animation()
                total_frames = self.sprite_sheets[current_anim]["frames"]
                self.animation_frame = (self.animation_frame + 1) % total_frames

            self.current_animation = self.get_current_animation()

        self.move(dt)
        self.attack(dt)

        if self.is_dying:
            # Blink effect using death_blink_speed
            current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
            if int(current_time / self.death_blink_speed) % 2 == 0:
                self.image.fill(self.color)
            else:
                self.image.fill((0, 0, 0))  # Blink to black

    def draw_debug_bounds(self, screen, frame_rect):
        """Draw debug visualization of collision and sprite bounds"""
        if SPRITE_SETTINGS["DEBUG_MODE"] and self.using_sprites:
            # Draw collision box in red
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
            # Draw sprite bounds in blue
            pygame.draw.rect(screen, (0, 0, 255), frame_rect, 2)

    def draw(self, screen):
        """Draw the character and attack range"""
        if self.is_dying and self.animation_complete:
            return

        if self.using_sprites and self.visible:
            current_frame = self.get_current_frame(self.current_animation)
            if current_frame:
                frame_rect = current_frame.get_rect()
                frame_rect.midbottom = self.rect.midbottom
                screen.blit(current_frame, frame_rect)
                
                # Draw attack range if attacking
                if self.attacking:
                    attack_rect = self.attack_range.get_rect()
                    if self.facing_right:
                        attack_rect.midleft = (frame_rect.centerx, frame_rect.centery)
                    else:
                        attack_rect.midright = (frame_rect.centerx, frame_rect.centery)
                    screen.blit(self.attack_range, attack_rect)
                
                # Debug visualization for all sprite-based characters
                self.draw_debug_bounds(screen, frame_rect)
        else:
            # Draw non-sprite character
            if self.visible:
                screen.blit(self.image, self.rect)
                if self.attacking:
                    attack_rect = self.attack_range.get_rect()
                    if self.facing_right:
                        attack_rect.midleft = self.rect.midright
                    else:
                        attack_rect.midright = self.rect.midleft
                    screen.blit(self.attack_range, attack_rect)

    def set_player_number(self, number):
        """
        sets player 1 or 2
        Args:
            number:number assigned to the player
        """
        self.player_number = number

class Regar(Character):
    def __init__(self, game):
        super().__init__("Regar", game=game)
        # Only load sprites in level screen
        if isinstance(self.game.current_screen, LevelScreen):
            self.using_sprites = True
            self.load_sprite_sheets()


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
        self.update_sprite()


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
        self.update_sprite()


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
