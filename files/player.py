from hero import Hero, Healer, Mage, Archer
from settings import get_tile_pos
from math import sqrt
from pathfinder import path_finder
from settings import box_settings


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None
        self.moved_hero = None
        self.path = None
        self.last_action = []
        self.actions = {
            "move": self.move,
            "basic": self.basic_attack,
            "special": self.special_skill
        }

    def set_starting_pos(self):
        if self.player_id == 1:
            return [Hero(0, [11, 0], side="west"), Archer(1, [11, 1], side="west")]
        else:
            return [Healer(0, [0, 0]), Mage(1, [0, 1])]

    def check_clicked_hero(self, clicked_pos):
        for hero in self.heroes:
            if get_tile_pos(clicked_pos) == hero.pos:
                self.clicked_hero = hero

    def action(self, opponent, object_tiles, clicked_pos, gui):
        if box_settings["BOX_WIDTH"] < clicked_pos[0] < box_settings["RIGHT_BOX"]:
            clicked_pos = get_tile_pos(clicked_pos)
            action_to_perform = gui.get_radio_value()
            return self.actions[action_to_perform](opponent, object_tiles, clicked_pos)

    def move(self, *args):
        opponent, object_tiles, pos = args
        if self.clicked_in_range(pos) and self.clicked_not_valid_tile(object_tiles, opponent, pos) is False:
            self.moved_hero = self.clicked_hero
            self.path = path_finder(self, opponent, object_tiles, pos)
            self.heroes[self.clicked_hero.hero_id].pos = pos
            self.clicked_hero = None
            return ["move", self.player_id, self.moved_hero, self.path]
        return False

    def basic_attack(self, *args):
        return self.clicked_hero.basic_attack(self, *args)
    
    def special_skill(self, *args):
        return self.clicked_hero.special_skill(self, *args)

    def clicked_own_hero(self, clicked_pos):
        try:
            return list(filter(lambda hero: clicked_pos == hero.pos, self.heroes))[0]
        except IndexError:
            return False

    def clicked_in_range(self, clicked_pos):
        distance = sqrt(sum([(i-j)**2 for i, j in zip(clicked_pos, self.clicked_hero.pos)]))
        return int(distance) <= self.clicked_hero.stats["RANGE"]

    @staticmethod
    def clicked_object(object_tiles, clicked_pos):
        return clicked_pos in object_tiles

    @staticmethod
    def clicked_opponent_hero(opponent, clicked_pos):
        try:
            return list(filter(lambda hero: clicked_pos == hero.pos, opponent.heroes))[0]
        except IndexError:
            return False

    def clicked_another_hero(self, opponent, clicked_pos):
        return self.clicked_opponent_hero(opponent, clicked_pos) or self.clicked_own_hero(clicked_pos)

    def clicked_not_valid_tile(self, object_tiles, opponent, clicked_pos):
        return self.clicked_object(object_tiles, clicked_pos) or self.clicked_another_hero(opponent, clicked_pos)
