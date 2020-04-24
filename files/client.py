import pygame as pg
from network import Network
import pickle
from files.player import Player
from files.tile_map import TiledMap
from files.settings import *
from os import path
pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
pg.font.init()
example_map = TiledMap('tmp_map.tmx', window)


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


def load_data(filename):
    game_folder = path.dirname(__file__)
    map_folder = path.join(game_folder, 'image')
    return path.join(map_folder, str(filename))


def draw_heroes(screen, player):
    for hero in player.heroes:
        hero_image = pg.image.load(load_data(HERO_IMAGES[str(hero.image_id)]))
        screen.blit(hero_image, coordinate(hero.pos))


def redrawWindow(screen, player1, player2):
    example_map.draw()
    draw_heroes(screen, player1)
    draw_heroes(screen, player2)
    pg.display.update()


def main():
    run = True
    clock = pg.time.Clock()
    n = Network()
    player1 = n.get_player()
    player_id = player1.player_id
    opponent_id = abs(player_id-1)
    opponent = None
    game_start = False
    turn = 0
    which_player_turn = 0

    while run:
        clock.tick(60)
        if game_start is False:
            try:
                data = n.send(["get_another_player", opponent_id])
                opponent = data[0]
                game_start = data[1]
            except:
                pass
        else:
            redrawWindow(window, player1, opponent)
            try:
                turns_data = n.send(["get_turn"])
                turn, which_player_turn = turns_data[0], turns_data[1]
            except:
                pass
            if which_player_turn == player_id:

                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if player1.clicked_hero is None:
                        player1.clicked_hero = check_clicked_hero(pos, player1.heroes)
                    else:
                        player1.move(get_tile_pos(pos))
                        n.send(["move", player_id, player1.heroes[player1.clicked_hero]])
                        player1.clicked_hero = None
            else:
                pass
                try:
                    opponent = n.send(["echo", opponent_id])
                except:
                    pass
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()



main()
