from math import sqrt
from pathfinder import path_finder
from abc import ABC, abstractmethod
import random


class HealthDisplay:
    def __init__(self, hero):
        self.hero = hero

    def __repr__(self):
        return str(self.hero.hp) + "/" + str(self.hero.max_hp)

    def __float__(self):
        return self.hero.hp / self.hero.max_hp


def update_stats(hero, hp_change):
    hero.hp += hp_change
    if hero.hp < 0:
        hero.hp = 0
    elif hero.hp > hero.max_hp:
        hero.hp = hero.max_hp
    hero.stats["HP"] = HealthDisplay(hero)
    return hero


class Hero(ABC):
    def __init__(self, hero_id, pos, attack, defense, move_range, hp, max_hp, skill_range, name,  side):
        self.hero_id = hero_id
        self.pos = pos
        self.side = side
        self.hp = hp
        self.max_hp = max_hp
        self.path = None
        self.stats = {
            "NAME": name,
            "HP": HealthDisplay(self),
            "ATTACK": attack,
            "DEFENSE": defense,
            "RANGE": move_range,
            "SKILL_RANGE": skill_range
        }
        self.actions = {
            "move": self.move,
            "basic": self.basic_attack,
            "special": self.special_skill
        }

    def in_range_of_skill(self, clicked_pos):
        distance = sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)]))
        return int(distance) <= self.stats["SKILL_RANGE"]

    def basic_attack(self, *args):
        player, opponent, object_tiles, clicked_pos = args
        distance = sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)]))
        attacked_hero = player.clicked_opp_hero(opponent, clicked_pos)
        if attacked_hero and distance < 2:
            attacking_hero = self
            lose_hp = -attacking_hero.stats["ATTACK"] + attacked_hero.stats["DEFENSE"]/2
            attacked_hero = update_stats(attacked_hero, lose_hp)
            opponent.heroes[attacked_hero.hero_id] = attacked_hero
            player.last_action = ["basic_attack", attacking_hero, attacked_hero]
            return["basic_attack", player.player_id, player.last_action]
        return False

    def move(self, *args):
        player, opponent, object_tiles, pos = args
        if player.clicked_in_range(pos) and player.clicked_not_valid_tile(object_tiles, opponent, pos) is False:
            player.moved_hero = self
            try:
                self.path = path_finder(player, opponent, object_tiles, pos)
            except IndexError:
                return False
            player.heroes[self.hero_id].pos = pos
            return ["move", player.player_id, self]
        return False

    @abstractmethod
    def special_skill(self, *args):
        pass


class Healer(Hero):
    def __init__(self, hero_id, pos, side):
        super().__init__(hero_id, pos, 5, 5, 3, 75, 75, 2, "HEALER", side)
        self.healing = 30

    def special_skill(self, *args):
        player, opponent, object_tiles, clicked_pos = args
        hero_to_heal = player.clicked_own_hero(clicked_pos)
        if hero_to_heal and self.in_range_of_skill(clicked_pos):
            hero_to_heal = update_stats(hero_to_heal, self.healing)
            player.heroes[hero_to_heal.hero_id] = hero_to_heal
            return ["heal", player.player_id, hero_to_heal]
        else:
            return False


class Mage(Hero):
    def __init__(self, hero_id, pos, side):
        super().__init__(hero_id, pos, 14, 7, 2, 50, 50, 10, "MAGE", side)

    def randomize_damage(self, hero):
        hero = update_stats(hero, -random.randrange(120, self.stats["ATTACK"]*15))
        return hero

    def special_skill(self, *args):
        player, opponent, object_tiles, clicked_pos = args
        heroes_to_attack = [player.clicked_opp_hero(opponent, clicked_pos)]
        if player.clicked_opp_hero(opponent, clicked_pos) and self.in_range_of_skill(clicked_pos):
            if len(opponent.heroes) > 1:
                heroes_to_attack.append(random.choice(opponent.heroes))
                heroes_to_attack = list(map(self.randomize_damage, heroes_to_attack))
            else:
                heroes_to_attack[0] = self.randomize_damage(heroes_to_attack[0])
            attacking_hero = player.clicked_hero
            player.last_action = ["random_spell", attacking_hero, heroes_to_attack]
            return ["random_spell", player.player_id, player.last_action]
        else:
            return False


class Warrior(Hero):
    def __init__(self, hero_id, pos, side):
        super().__init__(hero_id, pos, 10, 10, 5, 100, 100, 1, "WARRIOR", side)
        self.powerful_attack = 20

    def special_skill(self, *args):
        player, opponent, object_tiles, clicked_pos = args
        hero_to_attack = player.clicked_opp_hero(opponent, clicked_pos)
        if hero_to_attack and self.in_range_of_skill(clicked_pos):
            hero_to_attack = update_stats(hero_to_attack, -self.powerful_attack)
            attacking_hero = player.clicked_hero
            player.last_action = ["special_attack", attacking_hero, hero_to_attack]
            return ["special_attack", player.player_id, player.last_action]
        else:
            return False


class Archer(Hero):
    def __init__(self, hero_id, pos, side):
        super().__init__(hero_id, pos, 3, 3, 4, 55, 55, 7, "ARCHER", side)

    def special_skill(self, *args):
        player, opponent, object_tiles, clicked_pos = args
        hero_to_attack = player.clicked_opp_hero(opponent, clicked_pos)
        if hero_to_attack and self.in_range_of_skill(clicked_pos):
            multi = int(sqrt(sum([(i - j) ** 2 for i, j in zip(clicked_pos, self.pos)])))
            hero_to_attack = update_stats(hero_to_attack, -multi * self.stats["ATTACK"])
            attacking_hero = player.clicked_hero
            player.last_action = ["special_attack", attacking_hero, hero_to_attack]
            return ["special_attack", player.player_id, player.last_action]
        else:
            return False
