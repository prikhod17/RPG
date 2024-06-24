import random
import json


class Character:
    def __init__(self, name):
        self._name = name
        self._level = 1
        self._health = 100
        self._attack = 10
        self._defense = 5
        self._experience = 0
        self._crit_chance = 0.1
        self._crit_damage = 1.5
        self._inventory = Inventory()

    @property
    def name(self):
        return self._name

    @property
    def level(self):
        return self._level

    @property
    def health(self):
        return self._health

    @property
    def attack(self):
        return self._attack + self._inventory.total_attack_bonus

    @property
    def defense(self):
        return self._defense + self._inventory.total_defense_bonus

    @property
    def experience(self):
        return self._experience

    @property
    def inventory(self):
        return self._inventory

    def display_info(self):
        print(
            f"Name: {self.name}, Level: {self.level}, Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}, Experience: {self.experience}")

    def equip_item(self, item):
        if isinstance(item, InventoryItem):
            self._inventory.equip_item(item)
            print(f"{self.name} equipped {item.name}")
        else:
            print("Invalid item!")

    def unequip_item(self, item):
        if isinstance(item, InventoryItem):
            self._inventory.unequip_item(item)
            print(f"{self.name} unequipped {item.name}")
        else:
            print("Invalid item!")

    def attack_enemy(self, enemy):
        if isinstance(enemy, Character):
            crit = random.random() < self._crit_chance
            damage = random.randint(1, 10) * self.attack * (self._crit_damage if crit else 1) - enemy.defense
            if damage > 0:
                enemy._health -= damage
                print(f"{self.name} attacked {enemy.name} for {damage:.2f} damage{' (critical hit!)' if crit else ''}!")
                if enemy.health <= 0:
                    print(f"{enemy.name} has been defeated!")
                    self._experience += 10
            else:
                print(f"{self.name} missed the attack!")
        else:
            print("Invalid enemy!")


class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack += 5
        self._defense += 2


class Mage(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack += 2
        self._defense += 1


class Rogue(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack += 3
        self._defense += 1


class Paladin(Character):
    def __init__(self, name):
        super().__init__(name)
        self._attack += 4
        self._defense += 3


class InventoryItem:
    def __init__(self, name, item_type, attack_bonus=0, defense_bonus=0):
        self._name = name
        self._type = item_type
        self._attack_bonus = attack_bonus
        self._defense_bonus = defense_bonus

    @property
    def name(self):
        return self._name

    @property
    def item_type(self):
        return self._type

    @property
    def attack_bonus(self):
        return self._attack_bonus

    @property
    def defense_bonus(self):
        return self._defense_bonus


class Inventory:
    def __init__(self):
        self._items = []

    @property
    def items(self):
        return self._items

    @property
    def total_attack_bonus(self):
        return sum(item.attack_bonus for item in self._items)

    @property
    def total_defense_bonus(self):
        return sum(item.defense_bonus for item in self._items)

    def equip_item(self, item):
        if isinstance(item, InventoryItem):
            self._items.append(item)
        else:
            print("Invalid item!")

    def unequip_item(self, item):
        if isinstance(item, InventoryItem) and item in self._items:
            self._items.remove(item)
        else:
            print("Invalid item or item not equipped!")


class Game:
    def __init__(self):
        self.characters = []

    def add_character(self, character):
        if isinstance(character, Character):
            self.characters.append(character)
        else:
            print("Invalid character!")

    def battle(self, char1, char2):
        while char1.health > 0 and char2.health > 0:
            char1.attack_enemy(char2)
            if char2.health > 0:
                char2.attack_enemy(char1)
        if char1.health > 0:
            print(f"{char1.name} wins!")
        else:
            print(f"{char2.name} wins!")

    def save_game(self, filename):
        data = {
            "characters": [
                {
                    "name": char.name,
                    "level": char.level,
                    "health": char.health,
                    "attack": char.attack,
                    "defense": char.defense,
                    "experience": char.experience,
                    "inventory": [
                        {"name": item.name, "type": item.item_type, "attack_bonus": item.attack_bonus,
                         "defense_bonus": item.defense_bonus}
                        for item in char.inventory.items
                    ]
                }
                for char in self.characters
            ]
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Game saved to {filename}")

    def load_game(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
        self.characters = []
        for char_data in data["characters"]:
            char = Character(char_data["name"])
            char._level = char_data["level"]
            char._health = char_data["health"]
            char._attack = char_data["attack"]
            char._defense = char_data["defense"]
            char._experience = char_data["experience"]
            char._inventory = Inventory()
            for item_data in char_data["inventory"]:
                item = InventoryItem(item_data["name"], item_data["type"], item_data["attack_bonus"],
                                     item_data["defense_bonus"])
                char.equip_item(item)
            self.characters.append(char)
        print(f"Game loaded from {filename}")

