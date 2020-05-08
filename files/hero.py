class Hero:
    def __init__(self, hero_id, pos, attack=10, defense=10, move_range=5, hp=100, side="east", name="HERO"):
        self.hero_id = hero_id
        self.pos = pos
        self.side = side
        self.max_health = self.hp = hp
        self.attributes = {
            "NAME": name,
            "HP": str(self.hp) + "/" + str(self.max_health),
            "ATTACK": attack,
            "DEFENSE": defense,
            "RANGE": move_range
        }


class Healer(Hero):
    def __init__(self, hero_id, pos, side="east"):
        super().__init__(hero_id, pos, 5, 5, 3, 75, side=side, name="HEALER")

    def special_skill(self, *args):
        pass