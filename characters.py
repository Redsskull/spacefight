import pygame
from game_states import GameState
import logging
from typing import Optional, Tuple, List
from config import CHARACTER_STATS, ATTACK_SETTINGS

class Character(pygame.sprite.Sprite):
    """
    class for all characters in the game
    Args:
        pygame.sprite.Sprite: parent class
    """

    def __init__(self, name, game):
        """
        method to control the attributes of the characters
        Args:
            name: name of the character
            game: game object
        """
        super().__init__()
        # Get character stats from config
        stats = CHARACTER_STATS[name]
        self.name = name
        self.health = stats["health"]
        self.speed = stats["speed"]
        self.strength = stats["strength"]
        self.color = stats["color"]
        self.game = game
        
        # Create character sprite
        self.image = pygame.Surface((50, 100))
        self.image.fill(self.color)
        self.facing_right = True
        
        # Direction indicator
        self.direction_indicator = pygame.Surface((10, 10))
        self.direction_indicator.fill((0, 255, 0))
        
        self.update_sprite()
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.player_number = None
        
        # Attack properties
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = ATTACK_SETTINGS["cooldown"]
        self.attack_range = pygame.Surface(ATTACK_SETTINGS["range_size"])
        self.attack_range.fill(ATTACK_SETTINGS["range_color"])
        
        self.max_health = stats["health"]
        self.is_dying = False
        self.visible = True
        self.animation_complete = False
        self.blink_count = 0
        # Default timing values
        self.death_blink_duration = 0.2  # Time between blinks
        self.death_total_time = 2.0      # Total animation duration
        self.max_blinks = 10             # Number of blinks before death
        self.death_blink_timer = self.death_blink_duration

    def take_damage(self, amount: int) -> None:
        """Take damage"""
        self.health = max(0, self.health - amount)
        if self.health <= 0 and not self.is_dying:
            self.is_dying = True
            self.death_blink_timer = self.death_blink_duration
            self.animation_complete = False
            self.blink_count = 0

    def update_sprite(self):
        """
        method to update the sprite
        """
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
        """Perform attack
        Args:
            dt: time between frames
        """
        if not self.game.is_in_state(GameState.LEVEL):
            return

        if self.player_number == 1:
            # player 1 attack with left/right mouse buttons
            mouse = pygame.mouse.get_pressed()
            is_attacking = mouse[0] or mouse[2]  # left or right mouse button
        elif self.player_number == 2:
            # player 2 attacks with K_RCTRL (right ctrl) and K_RSHIFT (right shift)
            keys = pygame.key.get_pressed()
            is_attacking = keys[pygame.K_RCTRL] or keys[pygame.K_RSHIFT]

        if is_attacking and not self.attacking and self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            if self.game and hasattr(self.game, 'sound_manager'):
                try:
                    self.game.sound_manager.play_sound("punch")
                except AttributeError:
                    logging.warning("Sound manager not available")
            print(f"{self.name} (player {self.player_number}) is attacking")

        if self.attacking:
            attack_rect = self.attack_range.get_rect()
            if self.facing_right:
                attack_rect.midleft = (self.rect.centerx, self.rect.centery)
            else:
                attack_rect.midright = (self.rect.centerx, self.rect.centery)

            # Collision detection
            if self.game.is_in_state(GameState.LEVEL):
                if hasattr(self.game, 'enemy_manager'):
                    self.game.enemy_manager.handle_collision(attack_rect, self.strength)
                else:
                    logging.warning("Enemy manager not available")

        if self.attack_timer > 0:
            self.attack_timer -= dt
        else:
            self.attacking = False

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

        self.move(dt)
        self.attack(dt)

        if self.is_dying:
            # Blink effect using death_blink_speed
            current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
            if int(current_time / self.death_blink_speed) % 2 == 0:
                self.image.fill(self.color)
            else:
                self.image.fill((0, 0, 0))  # Blink to black

    def draw(self, screen):
        """Draw method with death animation support
        Args:
            screen: screen to draw on
        """
        if not self.visible or (self.is_dying and self.animation_complete):
            return

        screen.blit(self.image, self.rect)
        if self.attacking:
            attack_rect = self.attack_range.get_rect()
            if self.facing_right:
                attack_rect.midleft = (self.rect.centerx, self.rect.centery)
            else:
                attack_rect.midright = (self.rect.centerx, self.rect.centery)
            screen.blit(self.attack_range, attack_rect)

    def set_player_number(self, number):
        """
        sets player 1 or 2
        Args:
            number:number assigned to the player
        """
        self.player_number = number


class Regar(Character):
    """
        class for Regar character
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
        super().__init__("Regar", game=game)
        self.update_sprite()


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
