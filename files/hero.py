from math import sqrt


class HealthDisplay:
    def __init__(self, hero):
        self.hero = hero

    def __repr__(self):
        return str(self.hero.hp) + "\\" + str(self.hero.max_hp)

    def __float__(self):
        return self.hero.hp / self.hero.max_hp


class Hero:
    def __init__(self, hero_id, pos, attack=10, defense=10, move_range=5, hp=60, max_hp=100, side="east", name="HERO"):
        self.hero_id = hero_id
        self.pos = pos
        self.side = side
        self.hp = hp
        self.max_hp = max_hp
        self.stats = {
            "NAME": name,
            "HP": HealthDisplay(self),
            "ATTACK": attack,
            "DEFENSE": defense,
            "RANGE": move_range,
            "SKILL_RANGE": 0
        }

    def in_range_of_skill(self, clicked_pos):
        distance = sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)]))
        return int(distance) <= self.stats["SKILL_RANGE"]


class Healer(Hero):
    def __init__(self, hero_id, pos, side="east"):
        super().__init__(hero_id, pos, 5, 5, 3, 75, 75, side=side, name="HEALER")
        self.healing = 30
        self.stats["SKILL_RANGE"] = 2

    def special_skill(self, player, *args):
        opponent, object_tiles, clicked_pos = args
        hero_to_heal = player.clicked_own_hero(clicked_pos)
        if hero_to_heal and self.in_range_of_skill(clicked_pos):
            hero_to_heal.hp += self.healing
            if hero_to_heal.hp > hero_to_heal.max_hp:
                hero_to_heal.hp = 100
            hero_to_heal.stats["HP"] = HealthDisplay(hero_to_heal)
            player.heroes[hero_to_heal.hero_id] = hero_to_heal
            player.clicked_hero = None
            return ["heal", player.player_id, hero_to_heal]
        else:
            return False

