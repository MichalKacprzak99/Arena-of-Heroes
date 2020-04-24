import pygame as pg
from os import path


class Hero:
    def __init__(self, filename, hero_id, pos):
        self.image_id = 0#pg.image.load(self.load_data(filename))
        self.pos = pos
        self.hero_id = hero_id

    # @staticmethod
    def load_data(filename):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'image')
        return path.join(map_folder, str(filename))

