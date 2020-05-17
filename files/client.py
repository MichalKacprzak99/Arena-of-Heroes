import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import game_settings, box_settings, client_name, maps, mouse_button
from drawing import redraw_window
from menu import Menu
from gui import Gui


pg.init()
pg.font.init()


def main():
    run = True
    gui_start = False
    clock = pg.time.Clock()
    n = Network()
    player_id = n.get_player()
    pg.display.set_caption(client_name[str(player_id)])
    opponent_id = abs(player_id - 1)
    window = pg.display.set_mode((game_settings["GAME_SCREEN_WIDTH"], game_settings["GAME_SCREEN_HEIGHT"]))
    menu = Menu(window, n, player_id)

    while run:
        clock.tick(60)
        if not menu.both_ready():
            try:
                player, opponent, which_map, menu.opponent_ready = n.send(["get_info", opponent_id])
                board = TiledMap(maps[str(which_map)], window)
            except (EOFError, TypeError):
                break
            for event in pg.event.get():
                menu.highlight_buttons(event)
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
            if menu.player_ready:
                menu.loading_screen()
        else:
            if not gui_start:
                board.screen.fill((168, 139, 50))
                width = game_settings["GAME_SCREEN_WIDTH"] + box_settings["BOX_WIDTH"] * 2
                height = game_settings["GAME_SCREEN_HEIGHT"]
                window = pg.display.set_mode((width, height))

                gui = Gui(window, player, player_id, which_map)
                gui_start = True
            try:
                which_player_turn, turns = n.send(["get_turn", player_id])
            except TypeError:
                break
            try:
                actual_pos = pg.mouse.get_pos()
            except pg.error:
                break
            if opponent.last_action:
                player.react_to_event(opponent, n)

            gui.update_gui(actual_pos, player, opponent)
            player.check_result(opponent, n)
            move = redraw_window(window, board, player, opponent, which_player_turn, actual_pos, n)
            try:
                end = n.send(["end", player.player_id])
            except EOFError:
                break
            if end:
                pg.time.delay(3000)

                pg.quit()
                run = False
            else:
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
                    if event.type == pg.MOUSEBUTTONUP and event.button == mouse_button["RIGHT"]:
                        player.clicked_hero = None
                    if event.type == pg.MOUSEBUTTONUP and event.button == mouse_button["LEFT"]:
                        if which_player_turn == player_id:
                            gui.click(actual_pos, n)
                            if not player.clicked_hero:
                                player.check_clicked_hero(actual_pos)
                            else:
                                made_action = player.action(opponent, board.object_tiles, actual_pos, gui)
                                if made_action is not None:
                                    n.send(made_action)
                                    player.clicked_hero = None
                    try:
                        gui.menu.react(event)
                    except pg.error:
                        break
                try:
                    opponent = n.send(["echo", opponent_id])
                except EOFError:
                    break


if __name__ == '__main__':
    main()
