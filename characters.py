import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, name, health, speed, strength):
        super().__init__()
        self.name = name
        self.health = health
        self.speed = speed
        self.strength = strength
        self.image = pygame.Surface((50, 50))  # Placeholder rectangle
        self.image.fill((255, 0, 0))  # Red color as placeholder
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()

    def move(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
        
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
        
        movement = self.direction * self.speed * dt
        self.position += movement
        self.rect.topleft = int(self.position.x), int(self.position.y)

    def attack(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:  # Left mouse button
            print(f"{self.name} is attacking!")
            # Implement attack logic here

    def update(self, dt):
        self.move(dt)
        self.attack()

class Regar(Character):
    def __init__(self):
        super().__init__("Regar", health=120, speed=200, strength=10)
        self.image.fill((0, 0, 255))  # Blue color for Regar
    
    def special_ability(self):
        print("Regar uses his mighty strength!")
        # Implement Regar's special ability here

class Susan(Character):
    def __init__(self):
        super().__init__("Susan", health=100, speed=250, strength=8)
        self.image.fill((0, 255, 0))  # Green color for Susan
    
    def special_ability(self):
        print("Susan activates her tech gadgets!")
        # Implement Susan's special ability here

class Emily(Character):
    def __init__(self):
        super().__init__("Emily", health=90, speed=300, strength=7)
        self.image.fill((255, 255, 0))  # Yellow color for Emily
    
    def special_ability(self):
        print("Emily uses her agility to dodge!")
        # Implement Emily's special ability here

class Bart(Character):
    def __init__(self):
        super().__init__("Bart", health=150, speed=180, strength=12)
        self.image.fill((255, 0, 255))  # Magenta color for Bart
    
    def special_ability(self):
        print("Bart unleashes his brute force!")
        # Implement Bart's special ability here
