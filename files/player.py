from hero import Healer, Mage, Warrior, Archer
from settings import get_tile_pos
from math import sqrt
from settings import box_settings


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.death_heroes_pos = []
        self.clicked_hero = None
        self.moved_hero = None
        self.last_action = []

    def set_starting_pos(self):
        if self.player_id == 1:
            side = "west"
            return [Healer(0, [11, 1], side), Mage(1, [11, 4], side),  Warrior(2, [11, 7], side),  Archer(3, [11, 10], side)]
        else:
            return [Healer(0, [0, 1]), Mage(1, [0, 4]),  Warrior(2, [0, 7]),  Archer(3, [0, 10])]

    def check_clicked_hero(self, pos):
        for hero in self.heroes:
            if get_tile_pos(pos) == hero.pos:
                self.clicked_hero = hero

    def clicked_death_hero(self, pos):
        try:
            return list(filter(lambda death_hero_pos: death_hero_pos == pos, self.death_heroes_pos))[0]
        except IndexError:
            return False

    def action(self, opponent, object_tiles, pos, gui):
        if box_settings["BOX_WIDTH"] < pos[0] < box_settings["RIGHT_BOX"]:
            pos = get_tile_pos(pos)
            action_to_perform = gui.get_radio_value()
            return self.clicked_hero.actions[action_to_perform](self, opponent, object_tiles, pos)

    def clicked_own_hero(self, pos):
        try:
            return list(filter(lambda hero: pos == hero.pos, self.heroes))[0]
        except IndexError:
            return False

    def clicked_in_range(self, pos):
        distance = sqrt(sum([(i-j)**2 for i, j in zip(pos, self.clicked_hero.pos)]))
        return int(distance) <= self.clicked_hero.stats["RANGE"]

    @staticmethod
    def clicked_object(object_tiles, pos):
        return pos in object_tiles

    @staticmethod
    def clicked_opp_hero(opponent, pos):
        try:
            return list(filter(lambda hero: pos == hero.pos, opponent.heroes))[0]
        except IndexError:
            return False

    def clicked_another_hero(self, opponent, pos):
        return self.clicked_opp_hero(opponent, pos) or self.clicked_own_hero(pos) or self.clicked_death_hero(pos)

    def clicked_not_valid_tile(self, object_tiles, opponent, pos):
        return self.clicked_object(object_tiles, pos) or self.clicked_another_hero(opponent, pos)
