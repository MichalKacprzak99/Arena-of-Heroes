from abc import ABC, abstractmethod
from hero import HealthDisplay
import random
from pathfinder import create_matrix
import numpy as np


def create_potions(potions, player, opponent, object_tiles, net, seed):
    random.seed(seed)
    matrix = create_matrix(player, opponent, object_tiles)
    free_pos_y, free_pos_x = np.where(matrix == 1)
    free_pos = list(zip(free_pos_x, free_pos_y))
    positions = random.sample(free_pos, k=len(potions))
    for potion, cord in zip(potions, positions):
        potion.pos = cord
    net.send(["update_potions", potions])


class Potion(ABC):
    def __init__(self, name):
        self.name = name
        self.pos = [0, 0]

    @abstractmethod
    def affect(self, hero):
        pass


class HealthPotion(Potion):
    def __init__(self):
        super().__init__("HEALTH")
        self.heal_value = random.randint(10, 40)

    def affect(self, hero):
        hero.hp += self.heal_value
        if hero.hp > hero.max_hp:
            hero.hp = hero.max_hp
        hero.stats["HP"] = HealthDisplay(hero)


class AttackPotion(Potion):
    def __init__(self):
        super().__init__("ATTACK")
        self.attack_increase = random.randint(20, 40)

    def affect(self, hero):
        hero.stats["ATTACK"] += hero.stats["ATTACK"]*self.attack_increase/100


class SpeedPotion(Potion):
    def __init__(self):
        super().__init__("SPEED")
        self.range_increase = random.randint(1, 3)

    def affect(self, hero):
        hero.stats["RANGE"] += self.range_increase
        hero.stats["SKILL_RANGE"] += self.range_increase
