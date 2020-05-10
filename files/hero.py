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

    def basic_attack(self, player, *args):
        opponent, object_tiles, clicked_pos = args
        distance = sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)]))
        if player.clicked_opponent_hero(opponent, clicked_pos) and (distance <= 1) is True:
            attacking_hero = self
            attacked_hero = player.clicked_opponent_hero(opponent, clicked_pos)
            attacked_hero.hp -= attacking_hero.stats["ATTACK"] - attacked_hero.stats["DEFENSE"]/2
            attacked_hero.stats["HP"] = HealthDisplay(attacked_hero)
            opponent.heroes[attacked_hero.hero_id] = attacked_hero
            player.clicked_hero = None
            player.last_action = ["basic_attack", attacking_hero, attacked_hero]
            return["basic_attack", player.player_id, player.last_action]
        return False


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


class Mage(Hero):
    def __init__(self, hero_id, pos, side="east"):
        super().__init__(hero_id, pos, 14, 7, 2, 50, 50, side=side, name="MAGE")
        self.stats["SKILL_RANGE"] = 10

    def special_skill(self, player, *args):
        opponent, object_tiles, clicked_pos = args
        hero_to_attack = player.clicked_opponent_hero(opponent, clicked_pos)
        if hero_to_attack and self.in_range_of_skill(clicked_pos):
            hero_to_attack.hp -= self.stats["ATTACK"]
            if hero_to_attack.hp < 0:
                hero_to_attack.hp = 0
            hero_to_attack.stats["HP"] = HealthDisplay(hero_to_attack)
            attacking_hero = player.clicked_hero
            player.last_action = ["bolt", attacking_hero, hero_to_attack]
            player.clicked_hero = None
            return ["bolt", player.player_id, player.last_action]
        else:
            return False

