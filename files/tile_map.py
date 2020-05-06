import pytmx
from os import path
from settings import GAME_SETTINGS, BOX_SETTINGS
import pygame as pg

pg.init()
pg.font.init()
width = GAME_SETTINGS["GAME_SCREEN_WIDTH"]
height = GAME_SETTINGS["GAME_SCREEN_HEIGHT"]
window = pg.display.set_mode((width, height))


class TiledMap:
    def __init__(self, filename, screen):
        self.filename = self.load_data(filename)
        self.tmx_data = pytmx.load_pygame(self.filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.screen = screen
        self.map_img = self.make_map()
        self.object_tiles = self.get_objects_tiles()

    def draw(self):
        self.screen.blit(self.map_img, (BOX_SETTINGS["BOX_WIDTH"], 0))

    @staticmethod
    def load_data(filename):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        return path.join(map_folder, str(filename))

    def get_objects_tiles(self):
        tmp_list = []
        for tile_object in self.tmx_data.objects:
            tmp_list.append([int(tile_object.x)//64, int(tile_object.y)//64])
        return tmp_list

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                            y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
