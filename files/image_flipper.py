from settings import load_image
import pygame as pg
from os import path


def flip_image(image_to_flipped, name_of_flipped_image):
    game_folder = path.dirname(__file__)
    image_folder = path.join(game_folder, 'image')
    image_to_flip = pg.image.load(load_image(image_to_flipped))
    flipped_image = pg.transform.flip(image_to_flip, True, False)
    save_to = path.join(image_folder, str(name_of_flipped_image))
    pg.image.save(flipped_image, save_to)


flip_image("HEALER\\west.png", "HEALER\\east.png")
