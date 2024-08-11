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


class PlayerCharacter(Character):
    def __init__(self, name, health, speed, damage, size, special_attack):
        super().__init__(name, health, speed, damage, size)
        self.special_attack = special_attack

    def use_special_attack(self, target):
        #TODO: Implement special attack logic here
        pass

    def call_helper(self):
        # Implement helper call logic here
        pass


class HelperCharacter(Character):
    def __init__(self, name, health, speed, damage, size, helper_ability):
        super().__init__(name, health, speed, damage, size)
        self.helper_ability = helper_ability

    def use_helper_ability(self, target):
        #TODO: Implement helper ability logic here
        pass


class EnemyCharacter(Character):
    def __init__(self, name, health, speed, damage, size, enemy_type):
        super().__init__(name, health, speed, damage, size)
        self.enemy_type = enemy_type

class BossCharacter(Character):
    def __init__(self, name, health, speed, damage, size, boss_ability):
        super().__init__(name, health, speed, damage, size)
        self.boss_ability = boss_ability

    def use_boss_ability(self, target):
        #TODO: Implement boss ability logic here
        pass


    
