import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import WIDTH, HEIGHT, HERO_IMAGES, RED, CLIENT_NAME, coordinate, get_tile_pos, load_data
import pickle
pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.font.init()
example_map = TiledMap('map1.tmx', window)


def draw_player_turn(screen, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Player %d turn" % player_turn
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, RED)
    screen.blit(text, (WIDTH/2 - text_width/2, 20))


def highlight_tile(screen, pos):
    drawing_pos = coordinate(pos)
    pg.draw.rect(screen, RED, (drawing_pos[0], drawing_pos[1], 64, 64), 1)


def draw_if_clicked(screen):
    font = pg.font.SysFont("Arial", 15)
    text_to_input = "Clicked"
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, RED)
    screen.blit(text, (WIDTH/2 - text_width/2, 50))


def draw_heroes(screen, player):
    for hero in player.heroes:
        hero_image = pg.image.load(load_data(HERO_IMAGES[str(hero.image_id)]))
        screen.blit(hero_image, coordinate(hero.pos))


def redraw_window(screen, player1, player2, player_turn, clicked_hero, actual_pos):
    example_map.draw()
    highlight_tile(window, get_tile_pos(actual_pos))
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
    pg.display.set_caption(CLIENT_NAME[str(player_id)])
    print(("Hi, you are client: "+str(player_id)))
    opponent_id = abs(player_id - 1)
    game_start = False
    while run:
        clock.tick(60)
        if game_start is False:
            try:
                opponent, game_start = n.send(["get_another_player", opponent_id])
            except pickle.UnpicklingError:
                break
        else:
            which_player_turn, turns = n.send("get_turn")
            actual_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONUP:
                    if which_player_turn == player_id:
                        if player.clicked_hero is None:
                            player.check_clicked_hero(get_tile_pos(actual_pos))
                        else:
                            player.move(get_tile_pos(actual_pos))
                            moved_hero = player.heroes[player.clicked_hero]
                            n.send(["move", player_id, moved_hero])
                            player.clicked_hero = None
            opponent = n.send(["echo", opponent_id])
            redraw_window(window, player, opponent, which_player_turn, player.clicked_hero,actual_pos)


if __name__ == '__main__':
    main()
