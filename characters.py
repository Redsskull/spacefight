import math


class Character:
    def __init__(self, name, health, speed, damage, size):
        self.name = name
        self.health = health
        self.max_health = health
        self.speed = speed
        self.damage = damage
        self.size = size
        self.position = (0, 0)
        self.direction = "right"
        self.state = "idle"
        self.is_alive = True

    def move(self, dx, dy):
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            magnitude = math.sqrt(dx**2 + dy**2)
            dx = dx / magnitude
            dy = dy / magnitude

        new_x = self.position[0] + dx * self.speed
        new_y = self.position[1] + dy * self.speed
        self.position = (new_x, new_y)
        if dx != 0 or dy != 0:
            self.state = "walking"

            # determine direction(diaganol is important)
            if dx > 0:
                if dy > 0:
                    self.direction = "down_right"
                elif dy < 0:
                    self.direction = "up_right"
                else:
                    self.direction = "right"
            elif dx < 0:
                if dy > 0:
                    self.direction = "down_left"
                elif dy < 0:
                    self.direction = "up_left"
                else:
                    self.direction = "left"
            else:  # dx == 0
                if dy > 0:
                    self.direction = "down"
                else:  # dy < 0
                    self.direction = "up"
        else:
            self.state = "idle"

    def attack(self, target):
        target.health -= self.damage
        self.state = "attacking"

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_alive = False
            self.die()

    def die(self):
        self.state = "dead"
        self.direction = "down"

    def is_colliding(self, other):
        return (
            abs(self.position[0] - other.position[0]) < (self.size + other.size) / 2
            and abs(self.position[1] - other.position[1]) < (self.size + other.size) / 2
        )

    def get_targets_in_range(self, all_characters, range):
        targets_in_range = []
        for character in all_characters:
            if character != self and self.is_within_range(character, range):
                targets_in_range.append(character)
        return targets_in_range

    def is_within_range(self, target, range):
        # Example distance calculation, I'll replace with  game's logic
        dx = abs(self.position[0] - target.position[0])
        dy = abs(self.position[1] - target.position[1])
        distance = math.sqrt(dx**2 + dy**2)
        return distance <= range


class PlayerCharacter(Character):
    def __init__(self, name, health, speed, damage, size, special_attack=None):
        super().__init__(name, health, speed, damage, size)
        self.special_attack = special_attack  # This will be replaced by imported data
        self.helper = None  # Placeholder for helper character

    def use_special_attack(self, targets):
        # Placeholder for special attack logic
        return (
            self.special_attack(targets)
            if self.special_attack
            else "Default special attack"
        )


class HelperCharacter(Character):
    def __init__(self, name, health, speed, damage, size, helper_ability=None):
        super().__init__(name, health, speed, damage, size)
        self.helper_ability = helper_ability  # This will be replaced by imported data

    def use_helper_ability(self, targets):
        # Placeholder for helper ability logic
        return (
            self.helper_ability(targets)
            if self.helper_ability
            else "Default helper ability"
        )


class EnemyCharacter(Character):
    def __init__(self, name, health, speed, damage, size, enemy_type):
        super().__init__(name, health, speed, damage, size)
        self.enemy_type = enemy_type


class BossCharacter(Character):
    def __init__(self, name, health, speed, damage, size, boss_ability=None):
        super().__init__(name, health, speed, damage, size)
        self.boss_ability = boss_ability  # This will be replaced by imported data

    def use_boss_ability(self, target):
        # Placeholder for boss ability logic
        pass
