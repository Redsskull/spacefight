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
        self.helper = self.get_helper(name)

    def get_special_attack(self, name):
        special_attacks = {
            "Velscoundrel": self.velscoundrel_special,
            "Yuri": self.yuri_special,
            "Mike": self.mike_special,
            "Susan Calvin": self.susan_calvin_special,
        }
        return special_attacks.get(name, self.default_special)

    def get_helper(self, name):
        helpers = {
            "Velscoundrel": "Erok",
            "Yuri": "Barthlomew",
            "Mike": "Regar",
            "Susan Calvin": "Seniorita",
        }
        return helpers.get(name, "Generic Helper")

    def use_special_attack(self):
        targets = self.get_targets_in_range()
        return self.special_attack(targets)

    def velscoundrel_special(self, targets):
        return f"{self.name} stabs {targets}in the back!"

    def yuri_special(self, targets):
        return f"{self.name} bodyslams {targets}!"

    def mike_special(self, targets):
        return f"{self.name} shoots {targets}with a bazooka!"

    def susan_calvin_special(self, targets):
        return f"{self.name} uses a mind control ray on {targets}!"

    def default_special(self, targets):
        return f"{self.name} uses a special attack on {targets}!"

    def get_targets_in_range(self):
        # TODO: Implement target logic here after I have track of all characters and their positions
        return None

    def call_helper(self):
        return f"{self.name} calls {self.helper} for help!"


class HelperCharacter(Character):
    def __init__(self, name, health, speed, damage, size):
        super().__init__(name, health, speed, damage, size)
        self.helper_ability = self.get_helper_ability(name)

    def get_helper_ability(self, name):
        abilities = {
            "Erok": self.erok_ability,
            "Barthlomew": self.barthlomew_ability,
            "Regar": self.regar_ability,
            "Seniorita": self.seniorita_ability,
        }
        return abilities.get(name, self.default_ability)

    def use_helper_ability(self):
        targets = self.get_targets_in_range()
        return self.helper_ability(targets)

    def erok_ability(self, targets):
        return f"{self.name} runs away without doing anything! What a coward!"

    def barthlomew_ability(self, targets):
        return f"{self.name} uses a super bite and bleeds {targets} for massive damage!"

    def regar_ability(self, targets):
        return f"{self.name} swallows {targets} whole! hungry doggo!"

    def seniorita_ability(self, targets):
        return f"{self.name} confuses all enemies with her beauty!"

    def default_ability(self, targets):
        return f"{self.name} uses a helper ability on {targets}!"

    def get_targets_in_range(self):
        # TODO: Implement target logic here after I have track of all characters and their positions
        return None


class EnemyCharacter(Character):
    def __init__(self, name, health, speed, damage, size, enemy_type):
        super().__init__(name, health, speed, damage, size)
        self.enemy_type = enemy_type


class BossCharacter(Character):
    def __init__(self, name, health, speed, damage, size, boss_ability):
        super().__init__(name, health, speed, damage, size)
        self.boss_ability = boss_ability

    def use_boss_ability(self, target):
        # TODO: Implement boss ability logic here
        pass
