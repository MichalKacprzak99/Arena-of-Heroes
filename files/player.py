from hero import Hero
from settings import get_tile_pos
from math import sqrt
from pathfinder import path_finder


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None
        self.moved_hero = None
        self.list_of_tiles = None

    def set_starting_pos(self):
        if self.player_id == 1:
            return [Hero(0, 0, [11, 0], "west"), Hero(0, 1, [11, 1], "west")]
        else:
            return [Hero(0, 0, [0, 0]), Hero(0, 1, [0, 1])]

    def check_clicked_hero(self, clicked_pos):
        for hero in self.heroes:
            if get_tile_pos(clicked_pos) == hero.pos:
                self.clicked_hero = hero

    def action(self, opponent, object_tiles, clicked_pos):
        clicked_pos = get_tile_pos(clicked_pos)
        if self.clicked_hero.action == "move":
            return self.move(opponent, object_tiles, clicked_pos)
        return False

    def move(self, opponent, object_tiles, pos):
        if self.clicked_in_range(pos) and self.clicked_not_valid_tile(object_tiles, opponent, pos) is False:
            self.moved_hero = self.clicked_hero
            self.list_of_tiles = path_finder(self, opponent, object_tiles, pos)
            self.heroes[self.clicked_hero.hero_id].pos = pos
            self.clicked_hero = None
            return ["move", self.player_id, self.moved_hero, self.list_of_tiles]
        return False

    def clicked_own_hero(self, clicked_pos):
        return any(map(lambda hero: clicked_pos == hero.pos, self.heroes))

    def clicked_in_range(self, clicked_pos):
        distance = sqrt(sum([(i-j)**2 for i, j in zip(clicked_pos, self.clicked_hero.pos)]))
        return int(distance) <= self.clicked_hero.range

    @staticmethod
    def clicked_object(object_tiles, clicked_pos):
        return clicked_pos in object_tiles

    @staticmethod
    def clicked_opponent_hero(opponent, clicked_pos):
        return any(map(lambda opp_hero: clicked_pos == opp_hero.pos, opponent.heroes))

    def clicked_another_hero(self, opponent, clicked_pos):
        return self.clicked_opponent_hero(opponent, clicked_pos) or self.clicked_own_hero(clicked_pos)

    def clicked_not_valid_tile(self, object_tiles, opponent, clicked_pos):
        return self.clicked_object(object_tiles, clicked_pos) or self.clicked_another_hero(opponent, clicked_pos)
