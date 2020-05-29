from abc import ABC, abstractmethod
from hero import HealthDisplay
import random
from pathfinder import create_matrix
import numpy as np


def create_potions(potions, player, opponent, object_tiles, net, seed):
    random.seed(seed)
    matrix = create_matrix(player, opponent, object_tiles)
    free_pos_x, free_pos_y = np.where(matrix == 0)
    free_pos = list(zip(free_pos_x, free_pos_y))
    positions = random.sample(free_pos, k=len(potions))
    for potion, cord in zip(potions, positions):
        potion.pos = cord
    net.send(["update_potions", potions])
    return potions


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
        self.value = random.randint(10, 40)
        self.value = 30

    def affect(self, hero):
        hero.hp += self.value
        if hero.hp > hero.max_hp:
            hero.hp = hero.max_hp
        hero.stats["HP"] = HealthDisplay(hero)
        return hero


