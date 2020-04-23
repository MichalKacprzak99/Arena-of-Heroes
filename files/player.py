from files.hero import Hero


def coordinate(tile_pos):
    x, y = tile_pos[0], tile_pos[1]
    return [x*80, y*80]


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = [Hero("Mag.png", 0, [0,0]), Hero("Mag.png", 1, [0, 1])]#lista
        self.clicked_hero = None

    def move(self, new_pos):
        hero_to_move = self.heroes[self.clicked_hero]
        hero_to_move.pos = new_pos

    def draw(self, screen):
        for hero in self.heroes:
            screen.blit(hero.image, coordinate(hero.pos))

        #pg.display.update()