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
            "death": "HEALER/death.png",
            "walking": {
                "east": "HEALER/healer_walking/right_walking/0_Astrologer_Walk_0",
                "west": "HEALER/healer_walking/left_walking/0_Astrologer_Walk_0",
                "south": "HEALER/healer_walking/front_walking/0_Astrologer_Walk_0",
                "north": "HEALER/healer_walking/back_walking/0_Astrologer_Walk_0"
            },
            "attacking": {
                "east": "HEALER/healer_attacking/right_attacking/0_astrologer_Attack_0",
                "west": "HEALER/healer_attacking/left_attacking/0_astrologer_Attack_0",
                "south": "HEALER/healer_attacking/front_attacking/0_astrologer_Attack_0",
                "north": "HEALER/healer_attacking/back_attacking/0_astrologer_Attack_0"
        }
    },
    "MAGE": {
        "north": "MAGE/north.png",
        "south": "MAGE/south.png",
        "east": "MAGE/east.png",
        "west": "MAGE/west.png",
        "death": "MAGE/death.png",
        "walking": {
            "east": "MAGE/mage_walking/right_walking/Right - Walking_0",
            "west": "MAGE/mage_walking/left_walking/Left - Walking_0",
            "south": "MAGE/mage_walking/front_walking/Front - Walking_0",
            "north": "MAGE/mage_walking/back_walking/Back - Walking_0"
        },
        "attacking": {
            "east": "MAGE/mage_attacking/right_attacking/0_mage_Attack_0",
            "west": "MAGE/mage_attacking/left_attacking/0_mage_Attack_0",
            "south": "MAGE/mage_attacking/front_attacking/0_mage_Attack_0",
            "north": "MAGE/mage_attacking/back_attacking/0_mage_Attack_0"
        }
    },
    "WARRIOR": {
        "north": "WARRIOR/north.png",
        "south": "WARRIOR/south.png",
        "east": "WARRIOR/east.png",
        "west": "WARRIOR/west.png",
        "death": "WARRIOR/death.png",
        "walking": {
            "east": "WARRIOR/warrior_walking/right_walking/0_Warrior_Walk_0",
            "west": "WARRIOR/warrior_walking/left_walking/0_Warrior_Walk_0",
            "south": "WARRIOR/warrior_walking/front_walking/0_Warrior_Walk_0",
            "north": "WARRIOR/warrior_walking/back_walking/0_Warrior_Walk_0"
        },
        "attacking": {
            "east": "WARRIOR/warrior_attacking/right_attacking/0_warrior_Attack_0",
            "west": "WARRIOR/warrior_attacking/left_attacking/0_warrior_Attack_0",
            "south": "WARRIOR/warrior_attacking/front_attacking/0_warrior_Attack_0",
            "north": "WARRIOR/warrior_attacking/back_attacking/0_warrior_Attack_0"
        }
    },
    "ARCHER": {
        "north": "ARCHER/north.png",
        "south": "ARCHER/south.png",
        "east": "ARCHER/east.png",
        "west": "ARCHER/west.png",
        "death": "ARCHER/death.png",
        "walking": {
            "east": "ARCHER/archer_walking/right_walking/0_Archer_Walk_0",
            "west": "ARCHER/archer_walking/left_walking/0_Archer_Walk_0",
            "south": "ARCHER/archer_walking/front_walking/0_Archer_Walk_0",
            "north": "ARCHER/archer_walking/back_walking/0_Archer_Walk_0"
        },
        "attacking": {
            "east": "ARCHER/archer_attacking/right_attacking/0_archer_Attack_0",
            "west": "ARCHER/archer_attacking/left_attacking/0_archer_Attack_0",
            "south": "ARCHER/archer_attacking/front_attacking/0_archer_Attack_0",
            "north": "ARCHER/archer_attacking/back_attacking/0_archer_Attack_0"
        }
    }
}
result = {
    "4": "RESULT/star_1.png",
    "3": "RESULT/star_1.png",
    "2": "RESULT/star_2.png",
    "1": "RESULT/star_3.png",
    "0": "RESULT/star_4.png"
}
potion_img = {
    "HEALTH": "POTION/hp_potion.png",
    "SPEED": "POTION/speed_potion.png",
    "ATTACK": "POTION/attack_potion.png"
}


def load_image(filename):
    game_folder = path.dirname(__file__)
    image_folder = path.join(game_folder, 'image')
    return path.join(image_folder, str(filename))


def get_tile_pos(pos):
    return [(pos[0] - box_sets["BOX_WIDTH"]) // tile_dim["width"], pos[1] // tile_dim["height"]]


def coordinate(tile_pos):
    return [tile_pos[0] * tile_dim["width"] + box_sets["BOX_WIDTH"], tile_pos[1] * tile_dim["height"]]


def index_error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return False
    return wrapper
