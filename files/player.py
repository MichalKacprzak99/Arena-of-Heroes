from hero import Hero
from settings import get_tile_pos


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None
        self.moved_hero = None

    def set_starting_pos(self):
        if self.player_id == 1:
            return [Hero(0, 0, [11, 0]), Hero(0, 1, [11, 1])]
        else:
            return [Hero(0, 0, [0, 0]), Hero(0, 1, [0, 1])]

    def move(self, new_pos):
        self.heroes[self.clicked_hero].pos = get_tile_pos(new_pos)

    def check_clicked_hero(self, clicked_pos):
        for hero in self.heroes:
            if get_tile_pos(clicked_pos) == hero.pos:
                self.clicked_hero = hero.hero_id
