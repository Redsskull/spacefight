characters_data = {
    # Player Characters
    "Velscoundrel": {
        "health": 100,
        "speed": 5,
        "damage": 10,
        "size": 1,
        "helper_character": "Erok",
        "special_attack": "Backstab",
        "story": "A gypsy rogue with a mysterious past...",
        "lines": ["Prepare to meet your maker!", "You won't see this coming!"],
    },
    "Lance Sergio": {
        "health": 120,
        "speed": 4,
        "damage": 15,
        "size": 2,
        "helper_character": "Seniorita Emily",
        "special_attack": "Pistol Whip",
        "story": "A cartel boss...",
        "lines": ["Justice will be served!", "Feel the weight of my hammer!"],
    },

    "Professor Erik:": {
        "health": 80,
        "speed": 6,
        "damage": 8,
        "size": 1.5,
        "helper_character": "Tara",
        "special_attack": "wheel chair smash",
        "story": "A wise old man...",
        "lines": ["What kind of idiot?!?", "I'm too old for this..."],
    },

    "Rambo": {
        "health": 150,
        "speed": 3,
        "damage": 20,
        "size": 2.5,
        "helper_character": "Bathlomew",
        "special_attack": "Machine Gun",
        "story": "War veteran...",
        "lines": ["I'm your worst nightmare!", "You're all going down!"],
    },

    # Helper Characters
    "Erok": {
        "health": 50,
        "speed": 3,
        "damage": 5,
        "size": 0.5,
        "helper_ability": "Run Away",
        "story": "A cowardly sidekick...",
        "lines": ["I'm outta here!", "Not my problem!"],
    },

    "Seniorita Emily": {
        "health": 60,
        "speed": 2,
        "damage": 10,
        "size": 1,
        "helper_ability": "Heal",
        "story": "A mysterious cartel cat enforcer...",
        "lines": ["I will mend your wounds.", "I am your salvation."],
    },

    "Tara": {
        "health": 40,
        "speed": 4,
        "damage": 5,
        "size": 0.5,
        "helper_ability": "Teleport",
        "story": "An old mans best friend...",
        "lines": ["I will take you to safety.", "I will protect you."],
    },

    "Bathlomew": {
        "health": 70,
        "speed": 1,
        "damage": 15,
        "size": 1.5,
        "helper_ability": "Berserk",
        "story": "A loyal war cat to his papa...",
        "lines": ["I will fight by your side.", "Papa time! papa time! papa time!"],
    },
    # Enemy Characters
    "Space ninja": {
        "health": 30,
        "speed": 2,
        "damage": 5,
        "size": 0.8,
        "enemy_type": "human",
        "story": "A common space pirate...",
        "lines": ["You're no match for me!", "Prepare to die!"],
    },
    # Boss Characters
    "Sneaky the bug lord": {
        "health": 500,
        "speed": 1,
        "damage": 50,
        "size": 5,
        "boss_ability": "bug spray",
        "story": "An ancient evil awakens...",
        "lines": ["Your end is near!", "Bow before my might!", "It's a bug! hahahaha"],
    },
}


# Function to retrieve character data by name
def get_character_data(name):
    return characters_data.get(name, None)
