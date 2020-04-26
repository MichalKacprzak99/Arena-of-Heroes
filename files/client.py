import pygame as pg
from network import Network
import pickle
from player import Player
from tile_map import TiledMap
from settings import *
from os import path

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Client B")
pg.font.init()
example_map = TiledMap('tmp_map.tmx', window)


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
    player = n.get_player()
    player_id = player.player_id
    print(("Hi, you are client: "+str(player_id)))
    opponent_id = abs(player_id - 1)
    game_start = False
    while run:
        clock.tick(60)
        if game_start is False:
            try:
                opponent, game_start = n.send(["get_another_player", opponent_id])

            except:
                pass
        else:
            which_player_turn, turns = n.send("get_turn")
            if which_player_turn == player_id:
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONUP:#oddzielny plik na obsługe akcji gracza
                        pos = pg.mouse.get_pos()
                        if player.clicked_hero is None:
                            player.clicked_hero = check_clicked_hero(pos, player.heroes)
                            print(player.clicked_hero)
                        else:
                            player.move(get_tile_pos(pos))
                            moved_hero = player.heroes[player.clicked_hero]
                            tmp = n.send(["move", player_id, moved_hero])
                            player.clicked_hero = None

            opponent = n.send(["echo", opponent_id])
            redrawWindow(window, player, opponent)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()


main()
