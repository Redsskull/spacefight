import pygame


class Character(pygame.sprite.Sprite):
    """
    class for all characters in the game
    """

    def __init__(self, name, health, speed, strength):
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
        self.color = (255, 0, 0)  # Default color is red
        self.image = pygame.Surface((50, 100))  # Placeholder rectangle
        self.image.fill(self.color)
        self.facing_right = True
        self.direction_indicator = pygame.Surface((10, 10))  # Placeholder rectangle
        self.direction_indicator.fill((0, 255, 0)) # Green color
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
        method to attack the character
        Args:
            dt: time between frames
        """
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:  # Left mouse button
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            print(f"{self.name} is attacking!")
            # Implement attack logic here
        elif mouse[2]:  # Right mouse button
            self.attacking = True
            self.attack_timer = self.attack_cooldown
            print(f"{self.name} is using powerful attack!")
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
        self.move(dt)
        self.attack(dt)

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

    def __init__(self):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Regar", health=120, speed=200, strength=10)
        self.color = (0,0,255) # Blue color for Regar
        self.image.fill(self.color)
        self.update_sprite()


class Susan(Character):
    """
        class for Susan character
    Args:
        Character: parent class
    """

    def __init__(self):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Susan", health=100, speed=250, strength=8)
        self.color = (0, 255, 0) # Green color for Susan
        self.image.fill(self.color)
        self.update_sprite()


class Emily(Character):
    """
        class for Emily character
    Args:
        Character: parent class
    """

    def __init__(self):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Emily", health=90, speed=300, strength=7)
        self.color = (255, 255, 0) # Yellow color for Emily
        self.image.fill(self.color)
        self.update_sprite()


class Bart(Character):
    """
        class for Bart character
    Args:
        Character: parent class
    """

    def __init__(self):
        """
        method to control the attributes of the character
        Args:
            name: name of the character
            health: health of the character
            speed: speed of the character
            strength: strength of the character
        """
        super().__init__("Bart", health=150, speed=180, strength=12)
        self.color = (255, 0, 255) # Magenta color for Bart
        self.image.fill(self.color)
        self.update_sprite()
