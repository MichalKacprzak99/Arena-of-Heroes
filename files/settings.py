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
GAME_SETTINGS = {
    "GAME_SCREEN_WIDTH": 768,
    "GAME_SCREEN_HEIGHT": 768,
}
BOX_SETTINGS = {
    "BOX_WIDTH": 120,
    "BOX_HEIGHT": 768,
    "LEFT_BOX_CENTER": 60,
    "RIGHT_BOX": 120 + GAME_SETTINGS["GAME_SCREEN_WIDTH"]
}


CLIENT_NAME = {
    "0": "CLIENT A",
    "1": "CLIENT B"
}
MAPS = {
    "0": "map1/map1.tmx"
}
HERO_IMAGES = {
    "HERO": {
        "north": "HERO/north.png",
        "south": "HERO/south.png",
        "east": "HERO/east.png",
        "west": "HERO/west.png"
    }
}


def load_image(filename):
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, 'image')
    return path.join(map_folder, str(filename))


def get_tile_pos(pos):
    return [(pos[0]-120)//64, pos[1]//64]


def coordinate(tile_pos):
    return [tile_pos[0]*64 + 120, tile_pos[1]*64]
