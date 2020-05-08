from os import path

# define some colors (R, G, B)
colors = {
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
game_settings = {
    "GAME_SCREEN_WIDTH": 768,
    "GAME_SCREEN_HEIGHT": 768,
}
mouse_button = {
    "LEFT": 1,
    "MIDDLE": 2,
    "RIGHT": 3,
    "SCROLL_UP": 4,
    "SCROLL_DOWN": 5
}
box_settings = {
    "BOX_WIDTH": 120,
    "BOX_HEIGHT": 768,
    "LEFT_BOX_CENTER": 60,
    "RIGHT_BOX": 120 + game_settings["GAME_SCREEN_WIDTH"]
}


client_name = {
    "0": "CLIENT A",
    "1": "CLIENT B"
}
maps = {
    "0": "map1/map1.tmx"
}
hero_images = {
    "HERO": {
        "north": "HERO/north.png",
        "south": "HERO/south.png",
        "east": "HERO/east.png",
        "west": "HERO/west.png"
    },
    "HEALER": {
            "north": "HEALER/north.png",
            "south": "HEALER/south.png",
            "east": "HEALER/east.png",
            "west": "HEALER/west.png"
        }
}


def load_image(filename):
    game_folder = path.dirname(__file__)
    image_folder = path.join(game_folder, 'image')
    return path.join(image_folder, str(filename))


def get_tile_pos(pos):
    return [(pos[0]-120)//64, pos[1]//64]


def coordinate(tile_pos):
    return [tile_pos[0]*64 + 120, tile_pos[1]*64]
