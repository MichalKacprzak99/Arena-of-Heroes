from os import path

# define some colors (R, G, B)
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BROWN": (106, 55, 5),
    "BLUE": (0, 0, 255),
    "GRAY": (128, 128, 128)
}

# game settings
WIDTH = 768
HEIGHT = 768

HERO_IMAGES = {
    "0": "Mag.png"
}
CLIENT_NAME = {
    "0": "CLIENT A",
    "1": "CLIENT B"
}
MAPS = {
    "0": "map1/map1.tmx"
}


def load_image(filename):
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, 'image')
    return path.join(map_folder, str(filename))


def get_tile_pos(pos):
    return list(map(lambda cord: cord//64, pos))


def coordinate(tile_pos):
    return list(map(lambda cord: cord*64, tile_pos))



