from hero import Hero, Healer, Mage
from settings import get_tile_pos
from math import sqrt
from settings import box_settings


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None
        self.moved_hero = None
        self.last_action = []

    def set_starting_pos(self):
        if self.player_id == 1:
            side = "west"
            return [Healer(0, [11, 1], side), Mage(1, [11, 4], side),  Mage(2, [11, 7], side),  Mage(3, [11, 10], side)]
        else:
            return [Healer(0, [0, 1]), Mage(1, [0, 4]),  Mage(2, [0, 7]),  Mage(3, [0, 10])]

    def check_clicked_hero(self, clicked_pos):
        for hero in self.heroes:
            if get_tile_pos(clicked_pos) == hero.pos:
                self.clicked_hero = hero

    def action(self, opponent, object_tiles, clicked_pos, gui):
        if box_settings["BOX_WIDTH"] < clicked_pos[0] < box_settings["RIGHT_BOX"]:
            clicked_pos = get_tile_pos(clicked_pos)
            action_to_perform = gui.get_radio_value()
            return self.clicked_hero.actions[action_to_perform](self, opponent, object_tiles, clicked_pos)

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
