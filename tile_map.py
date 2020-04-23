import pygame as pg
import pytmx

from os import path


class TiledMap:
    def __init__(self, filename, screen):#docelowo numer
        self.filename = self.load_data(filename)
        self.tmx_data = pytmx.load_pygame(self.filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.screen = screen
        self.map_img = self.make_map()

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.map_img, (0, 0))
        #pg.display.update()

    @staticmethod
    def load_data(filename):
        game_folder = path.dirname(__file__)
        map_folder = path.join(game_folder, 'maps')
        return path.join(map_folder, str(filename))

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