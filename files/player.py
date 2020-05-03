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

    def check_clicked_hero(self, clicked_pos):
        for hero in self.heroes:
            if get_tile_pos(clicked_pos) == hero.pos:
                self.clicked_hero = hero.hero_id

    def move(self, new_pos):
        self.heroes[self.clicked_hero].pos = get_tile_pos(new_pos)
        moved_hero = self.heroes[self.clicked_hero]
        self.clicked_hero = None
        return ["move", self.player_id, moved_hero]

    def clicked_own_hero(self, clicked_pos):
        if any(map(lambda hero: clicked_pos == hero.pos, self.heroes)):
            return False
        else:
            return True

    @staticmethod
    def clicked_object(object_tiles, clicked_pos):
        return clicked_pos in object_tiles

    @staticmethod
    def clicked_opponent_hero(opponent, clicked_pos):
        return any(map(lambda opp_hero: clicked_pos == opp_hero.pos, opponent.heroes))

    def clicked_not_valid_tile(self, object_tiles, opponent, clicked_pos):
        return self.clicked_object(object_tiles, clicked_pos) or self.clicked_opponent_hero(opponent, clicked_pos)

    def action(self, opponent, object_tiles, clicked_pos):
        tmp_pos = get_tile_pos(clicked_pos)
        if self.clicked_own_hero(tmp_pos) is False:
            return False
        if self.clicked_not_valid_tile(object_tiles, opponent, clicked_pos) is False:
            return self.move(clicked_pos)
        else:
            return False


