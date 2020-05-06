import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import WIDTH, HEIGHT, CLIENT_NAME, MAPS
from drawing import redraw_window
from menu import Menu

pg.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.font.init()


def main():
    run = True
    clock = pg.time.Clock()
    n = Network()
    player = n.get_player()
    player_id = player.player_id
    pg.display.set_caption(CLIENT_NAME[str(player_id)])
    print(("Hi, you are client: "+str(player_id)))
    opponent_id = abs(player_id - 1)
    menu = Menu(window)
    while run:
        clock.tick(60)
        if menu.both_ready() is False:
            try:
                opponent, which_map, menu.opponent_ready = n.send(["get_info", opponent_id])
                board = TiledMap(MAPS[str(which_map)], window)
            except EOFError:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONUP:
                    actual_pos = pg.mouse.get_pos()
                    menu.click(actual_pos, n, player_id)
            if menu.player_ready is True:
                menu.loading_screen()
        else:
            try:
                which_player_turn, turns = n.send("get_turn")
            except EOFError:
                break
            actual_pos = pg.mouse.get_pos()
            redraw_window(window, board, player, opponent, which_player_turn, player.clicked_hero, actual_pos)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                    break
                if event.type == pg.MOUSEBUTTONUP:
                    if which_player_turn == player_id:
                        if player.clicked_hero is None:
                            player.check_clicked_hero(actual_pos)
                        else:
                            feedback = player.action(opponent, board.object_tiles, actual_pos)
                            if feedback:
                                n.send(feedback)
            try:
                opponent = n.send(["echo", opponent_id])
            except EOFError:
                break


if __name__ == '__main__':
    main()
