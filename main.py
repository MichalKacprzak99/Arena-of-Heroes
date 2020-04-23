import pygame
import sys
from player import Player
from hero import Hero
from tile_map import TiledMap
from settings import *
screen = pg.display.set_mode((WIDTH, HEIGHT))
pygame.init()
pygame.display.set_caption(TITLE)

def get_tile_pos(pos):
    x, y = pos[0], pos[1]
    return [int(x/80), int(y/80)]


def coordinate(tile_pos):
    x, y = tile_pos[0], tile_pos[1]
    return [x*80, y*80]


def check_clicked_hero(clicked_pos, heroes):
    clicked_tile = get_tile_pos(clicked_pos)
    for hero in heroes:
        if clicked_tile == hero.pos:
            return hero.hero_id
    return None


def main():
    example_map = TiledMap('tmp_map.tmx', screen)

    player = Player()
    hero_selected = False
    while True:
        example_map.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if player.clicked_hero is None:
                    player.clicked_hero = check_clicked_hero(pos, player.heroes)
                else:
                    player.move(get_tile_pos(pos))
                    player.clicked_hero = None

        player.draw(screen)
        pg.display.update()


main()
