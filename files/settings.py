from os import path

# define some colors (R, G, B)
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GREEN": (0, 255, 0),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "BROWN": (106, 55, 5),
    "BLUE": (0, 0, 255)
}

GUI_INFO = {
    "DISPLAY_HERO": 0,
    "HERO_NAME": 1,
    "DISPLAY_HP": 2,
    "HP_VALUE": 3,
    "DISPLAY_ATTACK": 4,
    "ATTACK_VALUE": 5,
    "DISPLAY_DEFENSE": 6,
    "DEFENSE_VALUE": 7,
    "OPPONENT_HERO": 8
}

# game settings
GAME_SCREEN_WIDTH = 768
GAME_SCREEN_HEIGHT = 768
BOX_WIDTH = 120
BOX_HEIGHT = 768
LEFT_BOX_CENTER = BOX_WIDTH/2
RIGHT_BOX_START = BOX_WIDTH + GAME_SCREEN_WIDTH

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
    return list(map(lambda cord: (cord - 120)//64, pos))


def coordinate(tile_pos):
    return list(map(lambda cord: cord*64 + 120, tile_pos))


def clicked_object(not_valid_tiles, clicked_pos):
    return clicked_pos not in not_valid_tiles


def clicked_opponent_hero(opponent, clicked_pos):
    return all(map(lambda opp_hero: clicked_pos != opp_hero.pos, opponent.heroes))