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
    "GRAY": (128, 128, 128),
    "BUMBLEBEE": (255, 226, 5),
    "ORANGE": (229, 83, 0)
}

tile_dim = {
    "width": 64,
    "height": 64,
}

game_sets = {
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

box_sets = {
    "BOX_WIDTH": 120,
    "BOX_HEIGHT": 768,
    "LEFT_BOX_CENTER": 60,
    "RIGHT_BOX": 120 + game_sets["GAME_SCREEN_WIDTH"]
}

client_name = {
    "0": "CLIENT A",
    "1": "CLIENT B"
}

maps = {
    "0": "jungle/jungle.tmx",
    "1": "western/western.tmx",
    "2": "autumn/autumn.tmx",
    "3": "winter/winter.tmx"
}

backgrounds = {
    "0": "backgrounds/jungle_background.png",
    "1": "backgrounds/wild_west_background.png",
    "2": "backgrounds/arena_background.png",
    "3": "backgrounds/winter_background.png"
}

icons = {
    "hp": "image/icons/hp_icon_resized.png",
    "attack": "image/icons/attack_icon_resized.png",
    "defense": "image/icons/defense_icon_resized.png",
    "range": "image/icons/range_icon_resized.png",
    "special": "image/icons/special_icon_resized.png"
}


hero_images = {
    "HEALER": {
            "north": "HEALER/north.png",
            "south": "HEALER/south.png",
            "east": "HEALER/east.png",
            "west": "HEALER/west.png",
            "death": "HEALER/death.png"
    },
    "MAGE": {
        "north": "MAGE/north.png",
        "south": "MAGE/south.png",
        "east": "MAGE/east.png",
        "west": "MAGE/west.png",
        "death": "MAGE/death.png"
    },
    "WARRIOR": {
        "north": "WARRIOR/north.png",
        "south": "WARRIOR/south.png",
        "east": "WARRIOR/east.png",
        "west": "WARRIOR/west.png",
        "death": "WARRIOR/death.png"
    },
    "ARCHER": {
        "north": "ARCHER/north.png",
        "south": "ARCHER/south.png",
        "east": "ARCHER/east.png",
        "west": "ARCHER/west.png",
        "death": "ARCHER/death.png"
    }
}
result = {
    "4": "RESULT/star_1.png",
    "3": "RESULT/star_1.png",
    "2": "RESULT/star_2.png",
    "1": "RESULT/star_3.png",
    "0": "RESULT/star_4.png"
}


def load_image(filename):
    game_folder = path.dirname(__file__)
    image_folder = path.join(game_folder, 'image')
    return path.join(image_folder, str(filename))


def get_tile_pos(pos):
    return [(pos[0] - box_sets["BOX_WIDTH"]) // tile_dim["width"], pos[1] // tile_dim["height"]]


def coordinate(tile_pos):
    return [tile_pos[0] * tile_dim["width"] + box_sets["BOX_WIDTH"], tile_pos[1] * tile_dim["height"]]
