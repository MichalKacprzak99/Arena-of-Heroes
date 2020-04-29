from files.hero import Hero
import pygame as pg
from settings import get_tile_pos, coordinate


def check_clicked_hero(clicked_pos, heroes):
    clicked_tile = get_tile_pos(clicked_pos)
    for hero in heroes:
        if clicked_tile == hero.pos:
            return hero.hero_id
    return None


class Player:
    def __init__(self, name="", player_id=0):
        self.name = name
        self.player_id = player_id
        self.heroes = self.set_starting_pos()
        self.clicked_hero = None
        self.moved_hero = None

    def set_starting_pos(self):
        if self.player_id == 1:
            return [Hero("Mag.png", 0, [9, 0]), Hero("Mag.png", 1, [9, 1])]
        else:
            return [Hero("Mag.png", 0, [0, 0]), Hero("Mag.png", 1, [0, 1])]

    def move(self, new_pos):
        self.heroes[self.clicked_hero].pos = new_pos
