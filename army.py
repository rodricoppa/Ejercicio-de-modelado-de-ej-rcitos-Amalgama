from abc import ABC, abstractmethod


# ---------- Units ----------

class Unit(ABC):
    def __init__(self, years):
        self.years = years
        self.strength = 0

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def transform(self):
        pass


class Pikeman(Unit):
    def __init__(self, years):
        super().__init__(years)
        self.strength = 5

    def train(self):
        self.strength += 3
        return 10  # gold cost

    def transform(self):
        return Archer(self.years), 30


class Archer(Unit):
    def __init__(self, years):
        super().__init__(years)
        self.strength = 10

    def train(self):
        self.strength += 7
        return 20

    def transform(self):
        return Knight(self.years), 40


class Knight(Unit):
    def __init__(self, years):
        super().__init__(years)
        self.strength = 20

    def train(self):
        self.strength += 10
        return 30

    def transform(self):
        return None, 0  # cannot transform


# ---------- Army ----------

CIVILIZATIONS = {
    "Chinese": {"pikeman": 2, "archer": 25, "knight": 2},
    "English": {"pikeman": 10, "archer": 10, "knight": 10},
    "Byzantine": {"pikeman": 5, "archer": 8, "knight": 15},
}


class Army:
    def __init__(self, civilization):
        self.civilization = civilization
        self.gold = 1000
        self.units = []
        self.battles = []

        self._create_initial_units()

    def _create_initial_units(self):
        config = CIVILIZATIONS[self.civilization]

        for _ in range(config["pikeman"]):
            self.units.append(Pikeman(years=0))

        for _ in range(config["archer"]):
            self.units.append(Archer(years=0))

        for _ in range(config["knight"]):
            self.units.append(Knight(years=0))

    def total_strength(self):
        return sum(unit.strength for unit in self.units)

    def lose_strongest_units(self, amount):
        self.units.sort(key=lambda u: u.strength, reverse=True)
        self.units = self.units[amount:]

    def attack(self, other_army):
        my_strength = self.total_strength()
        enemy_strength = other_army.total_strength()

        if my_strength > enemy_strength:
            other_army.lose_strongest_units(2)
            self.gold += 100
            self.battles.append("Win")
            other_army.battles.append("Loss")

        elif my_strength < enemy_strength:
            self.lose_strongest_units(2)
            other_army.gold += 100
            self.battles.append("Loss")
            other_army.battles.append("Win")

        else:
            # tie
            if self.units:
                self.lose_strongest_units(1)
            if other_army.units:
                other_army.lose_strongest_units(1)

            self.battles.append("Tie")
            other_army.battles.append("Tie")
