import pygame
import sys
from os import path
from tile_map import TiledMap
from settings import *
screen = pg.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption(TITLE)


def main():
    example_map = TiledMap('tmp_map.tmx', screen)
    example_map.draw()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()


main()
