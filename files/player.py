from hero import Healer, Mage, Warrior, Archer
from settings import get_tile_pos, box_settings
from math import sqrt


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.death_heroes_pos = []
        self.clicked_hero = None
        self.moved_hero = None
        self.attacking_hero = None
        self.last_action = []
        self.result = ""

    def set_starting_pos(self):
        pos = iter([[11*self.player_id, i] for i in range(1, 11, 3)])
        side = "west" if self.player_id == 1 else "east"
        return [Healer(0, next(pos), side), Mage(1, next(pos), side),
                Warrior(2, next(pos), side), Archer(3, next(pos), side)]

    def add_death_heroes(self, death_heroes):
        death_heroes = sorted(death_heroes, key=lambda sorted_hero: sorted_hero.hero_id, reverse=True)
        for death_hero in death_heroes:
            self.death_heroes_pos.append(death_hero)
            del self.heroes[death_hero.hero_id]
            if len(self.heroes):
                for hero in self.heroes[death_hero.hero_id:]:
                    hero.hero_id -= 1

    def react_to_event(self, opponent, n):
        reaction = ["basic_attack", "special_attack"]
        dead_heroes = []
        if opponent.last_action[0] in reaction:
            attacked_hero = opponent.last_action[2]
            self.heroes[attacked_hero.hero_id] = attacked_hero
            if self.heroes[attacked_hero.hero_id].hp == 0:
                dead_heroes.append(self.heroes[attacked_hero.hero_id])
        elif opponent.last_action[0] == "random_spell":
            attacked_heroes = opponent.last_action[2]
            for attacked_hero in attacked_heroes:
                self.heroes[attacked_hero.hero_id] = attacked_hero
                if attacked_hero.hp == 0 and attacked_hero not in dead_heroes:
                    dead_heroes.append(attacked_hero)
        self.add_death_heroes(dead_heroes)

        n.send(["reset_action", opponent.player_id])
        n.send(["death_heroes", self.player_id, self.heroes, self.death_heroes_pos])
        opponent.last_action = None

    def check_result(self, opponent, n):
        if len(self.heroes) == 0:
            self.result = "lose"
        elif len(opponent.heroes) == 0:
            self.result = "win"
        try:
            n.send(["result", self.player_id, self.result])
        except EOFError:
            pass

    def action(self, opponent, object_tiles, pos, gui):
        if box_settings["BOX_WIDTH"] < pos[0] < box_settings["RIGHT_BOX"]:
            pos = get_tile_pos(pos)
            action_to_perform = gui.get_radio_value()
            return self.clicked_hero.actions[action_to_perform](self, opponent, object_tiles, pos)

    def check_clicked_hero(self, pos):
        for hero in self.heroes:
            if get_tile_pos(pos) == hero.pos:
                self.clicked_hero = hero

    def clicked_death_hero(self, pos):
        try:
            return list(filter(lambda death_hero_pos: death_hero_pos.pos == pos, self.death_heroes_pos))[0]
        except IndexError:
            return False

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
