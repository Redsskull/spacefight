import pygame
from characters import Regar, Susan, Emily, Bart

class CharacterManager:
    def __init__(self, game):
        self.game = game
        self.characters = [Regar(), Susan(), Emily(), Bart()]
        self.character_group = pygame.sprite.Group()
        for character in self.characters:
            self.character_group.add(character)

    def initialize_characters(self):
        station_width = (self.game.SCREEN_WIDTH - 150) // 4
        for i, character in enumerate(self.characters):
            x = 75 + i * (station_width + 25)
            y = 300
            character.rect.topleft = (x, y)
            character.position = pygame.math.Vector2(x, y)

    def draw_characters(self, screen):
        self.character_group.draw(screen)

    def get_character_by_name(self, name):
        return next((char for char in self.characters if char.name == name), None)

    def update_characters(self, dt):
        for character in self.characters:
            character.update(dt)

    def handle_character_movement(self, dt):
        keys = pygame.key.get_pressed()
        for character in self.characters:
            character.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
            character.direction.y = keys[pygame.K_s] - keys[pygame.K_w]
            character.move(dt)

    def handle_character_attack(self):
        mouse = pygame.mouse.get_pressed()
        if mouse[0] or mouse[2]:  # Left or right mouse button
            for character in self.characters:
                character.attack()

    def get_character_info(self):
        return [(char.name, char.health, char.speed, char.strength) for char in self.characters]
