from files.hero import Hero


def coordinate(tile_pos):
    x, y = tile_pos[0], tile_pos[1]
    return [x*80, y*80]


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None

    def set_starting_pos(self):
        if self.player_id == 1:
            return [Hero("Mag.png", 0, [9, 0]), Hero("Mag.png", 1, [9, 1])]
        else:
            return [Hero("Mag.png", 0, [0, 0]), Hero("Mag.png", 1, [0, 1])]

    def move(self, new_pos):
        self.heroes[self.clicked_hero].pos = new_pos
