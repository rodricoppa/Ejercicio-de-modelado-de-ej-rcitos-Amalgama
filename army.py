# ---------- Units ----------

class Unit:
    def __init__(self, years):
        self.years = years
        self.strength = 0

    def train(self):
        raise NotImplementedError

    def transform(self):
        return None


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
        return None  # knights cannot transform


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

        self._create_units()

    def _create_units(self):
        data = CIVILIZATIONS[self.civilization]

        for _ in range(data["pikeman"]):
            self.units.append(Pikeman(0))

        for _ in range(data["archer"]):
            self.units.append(Archer(0))

        for _ in range(data["knight"]):
            self.units.append(Knight(0))

    def total_strength(self):
        total = 0
        for unit in self.units:
            total += unit.strength
        return total

    def remove_strongest_units(self, count):
        self.units.sort(key=lambda u: u.strength, reverse=True)
        self.units = self.units[count:]

    def attack(self, other_army):
        my_strength = self.total_strength()
        enemy_strength = other_army.total_strength()

        if my_strength > enemy_strength:
            other_army.remove_strongest_units(2)
            self.gold += 100
            self.battles.append("Win")
            other_army.battles.append("Loss")

        elif my_strength < enemy_strength:
            self.remove_strongest_units(2)
            other_army.gold += 100
            self.battles.append("Loss")
            other_army.battles.append("Win")

        else:
            # tie: both armies lose one unit
            if self.units:
                self.remove_strongest_units(1)
            if other_army.units:
                other_army.remove_strongest_units(1)

            self.battles.append("Tie")
            other_army.battles.append("Tie")
