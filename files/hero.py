from math import sqrt


class Hero:
    def __init__(self, hero_id, pos, attack=10, defense=10, move_range=5, hp=60, max_hp=100, side="east", name="HERO"):
        self.hero_id = hero_id
        self.pos = pos
        self.side = side
        self.stats = {
            "NAME": name,
            "HP": hp,
            "MAX_HP": max_hp,
            "ATTACK": attack,
            "DEFENSE": defense,
            "RANGE": move_range
        }


class Healer(Hero):
    def __init__(self, hero_id, pos, side="east"):
        super().__init__(hero_id, pos, 5, 5, 3, 75, 75, side=side, name="HEALER")
        self.healing = 30
        self.stats["SKILL_RANGE"] = 2

    def special_skill(self, player, *args):
        opponent, object_tiles, clicked_pos = args
        hero_to_heal = player.clicked_own_hero(clicked_pos)
        if hero_to_heal and self.in_range_of_healing(clicked_pos):
            hero_to_heal.stats["HP"] += self.healing
            if hero_to_heal.stats["HP"] > hero_to_heal.stats["MAX_HP"]:
                hero_to_heal.stats["HP"] = 100
            player.heroes[hero_to_heal.hero_id] = hero_to_heal
            player.clicked_hero = None
            return ["heal", player.player_id, hero_to_heal]
        else:
            return False

    def in_range_of_healing(self, clicked_pos):
        distance = sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)]))
        return int(distance) <= self.stats["SKILL_RANGE"]
