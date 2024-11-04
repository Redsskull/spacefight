import pygame
from game_states import GameState


class Character(pygame.sprite.Sprite):
    """
    class for all characters in the game
    """

    def __init__(self, name, health, speed, strength, game):
        """
        method to control the attributes of the characters
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__()
        self.name = name
        self.health = health
        self.speed = speed
        self.strength = strength
        self.game = game
        self.color = (255, 0, 0)  # Default color is red
        self.image = pygame.Surface((50, 100))  # Placeholder rectangle
        self.image.fill(self.color)
        self.facing_right = True
        self.direction_indicator = pygame.Surface((10, 10))  # Placeholder rectangle
        self.direction_indicator.fill((0, 255, 0))  # Green color
        self.update_sprite()
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.player_number = None  # May have to change to 0
        self.attacking = False
        self.attack_cooldown = 0.1  # 0.5 seconds between attacks
        self.attack_timer = 0
        self.attack_range = pygame.Surface((50, 100))  # Placeholder rectangle
        self.attack_range.fill((144, 238, 144))  # Light green colort
        self.max_health = health
        self.health = health
        self.is_dying = False
        self.death_blink_timer = 0
        self.death_blink_duration = 0.05
        self.death_total_time = 0.5
        self.visible = True
        self.animation_complete = False
        self.blink_count = 0
        self.max_blinks = 5

    def take_damage(self, amount):
        """
        method to control the damage taken by the character
        Args:
            amount: amount of damage taken
        """
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

    def move(self, dt):
        """
        method to control the character movements
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

    def attack(self, dt):
        """
        method to control the character attacks
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
            if self.game:
                self.game.sound_manager.play_sound("punch")
            print(f"{self.name} (player {self.player_number}) is attacking")

        if self.attacking:
            attack_rect = self.attack_range.get_rect()
            if self.facing_right:
                attack_rect.midleft = (self.rect.centerx, self.rect.centery)
            else:
                attack_rect.midright = (self.rect.centerx, self.rect.centery)

            # Collision detection
            if self.game.is_in_state(GameState.LEVEL):
                self.game.enemy_manager.handle_collision(attack_rect, self.strength)

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

    def draw(self, screen):
        """Draw method with death animation support"""
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
        super().__init__("Regar", health=120, speed=200, strength=10, game=game)
        self.color = (0, 0, 255)  # Blue color for Regar
        self.image.fill(self.color)
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
        super().__init__("Susan", health=100, speed=250, strength=8, game=game)
        self.color = (0, 255, 0)  # Green color for Susan
        self.image.fill(self.color)
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
        super().__init__("Emily", health=90, speed=300, strength=7, game=game)
        self.color = (255, 255, 0)  # Yellow color for Emily
        self.image.fill(self.color)
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
        super().__init__("Bart", health=150, speed=180, strength=12, game=game)
        self.color = (255, 0, 255)  # Magenta color for Bart
        self.image.fill(self.color)
        self.update_sprite()
