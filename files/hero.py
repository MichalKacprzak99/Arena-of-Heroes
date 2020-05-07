class Hero:
    def __init__(self, hero_id, pos, attack=10, defense=10, move_range=5, hp=100, which_side="east", name="HERO"):
        self.hero_id = hero_id
        self.pos = pos
        self.which_side = which_side
        self.max_health = self.hp = hp
        self.attributes = {
            "NAME": name,
            "MAX HP": self.max_health,
            "HP": self.hp,
            "ATTACK": attack,
            "DEFENSE": defense,
            "RANGE": move_range
        }


class Healer(Hero):
    def __init__(self, hero_id, pos, which_side="east"):
        super().__init__(hero_id, pos, 5, 5, 3, 75, which_side=which_side, name="Michal")

    def special_skill(self, *args):
        pass