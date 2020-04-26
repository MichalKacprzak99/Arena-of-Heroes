import pygame as pg
from network import Network
import pickle
from player import Player
from tile_map import TiledMap
from settings import *
from os import path

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
pg.font.init()
example_map = TiledMap('tmp_map.tmx', window)


def draw_player_turn(screen, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Player %d turn" % player_turn
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, RED)
    screen.blit(text, (WIDTH/2 - text_width/2, 20))


def draw_if_clicked(screen):
    font = pg.font.SysFont("Arial", 15)
    text_to_input = "Clicked"
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, RED)
    screen.blit(text, (WIDTH/2 - text_width/2, 50))
    pg.display.update()


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


def redraw_window(screen, player1, player2, player_turn, clicked_hero):
    example_map.draw()
    draw_heroes(screen, player1)
    draw_heroes(screen, player2)
    draw_player_turn(screen, player_turn)
    if clicked_hero is not None:
        draw_if_clicked(window)
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
            opponent = n.send(["echo", opponent_id])
            redraw_window(window, player, opponent, which_player_turn, player.clicked_hero)
            if which_player_turn == player_id:
                action = player.handle_action(opponent)
                if action is not None:
                    tmp = n.send(action)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()


main()