import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import GAME_SETTINGS, BOX_SETTINGS, CLIENT_NAME, MAPS
from drawing import redraw_window
from menu import Menu
from gui import Gui


pg.init()
beginning = pg.display.set_mode((GAME_SETTINGS["GAME_SCREEN_WIDTH"], GAME_SETTINGS["GAME_SCREEN_HEIGHT"]-125))
pg.font.init()


def main():
    run = True
    gui_start = False
    clock = pg.time.Clock()
    n = Network()
    player = n.get_player()
    player_id = player.player_id
    pg.display.set_caption(CLIENT_NAME[str(player_id)])
    print(("Hi, you are client: "+str(player_id)))
    opponent_id = abs(player_id - 1)
    menu = Menu(beginning)

    while run:
        clock.tick(60)
        if menu.both_ready() is False:
            try:
                opponent, which_map, menu.opponent_ready = n.send(["get_info", opponent_id])
                board = TiledMap(MAPS[str(which_map)], beginning)
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
            if not gui_start:
                width = GAME_SETTINGS["GAME_SCREEN_WIDTH"] + BOX_SETTINGS["BOX_WIDTH"] * 2
                height = GAME_SETTINGS["GAME_SCREEN_HEIGHT"]
                window = pg.display.set_mode((width, height))
                gui = Gui(window)
                gui_start = True
            try:
                which_player_turn, turns = n.send("get_turn")
            except EOFError:
                break
            actual_pos = pg.mouse.get_pos()

            gui.update_gui(actual_pos, player, opponent)

            move = redraw_window(window, board, player, opponent, which_player_turn, player.clicked_hero, actual_pos)
            if move:
                try:
                    n.send(["update", opponent_id])
                except EOFError:
                    break
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
