from os import path
#vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 800  # 16 * 48 or 32 * 24 or 64 * 12
#FPS = 60
BGCOLOR = BROWN
HERO_IMAGES = {
    "0": "Mag.png"
}
CLIENT_NAME = {
    "0": "CLIENT A",
    "1": "CLIENT B"
}


def load_data(filename):
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, 'image')
    return path.join(map_folder, str(filename))


def get_tile_pos(pos):
    x, y = pos[0], pos[1]
    return [int(x / 80), int(y / 80)]


def coordinate(tile_pos):
    x, y = tile_pos[0], tile_pos[1]
    return [x * 80, y * 80]