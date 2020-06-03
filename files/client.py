import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import game_sets, box_sets, client_name, maps, mouse_button
from drawing import redraw_window
from menu import Menu
from gui import Gui
from login import LoginScreen
from potions import create_potions
pg.init()
pg.font.init()


def main():
    run = True
    gui_start = False
    clock = pg.time.Clock()
    net = Network()
    player_id = net.get_player_id()
    pg.display.set_caption(client_name[str(player_id)])
    opponent_id = abs(player_id - 1)
    window = pg.display.set_mode((game_sets["GAME_SCREEN_WIDTH"], game_sets["GAME_SCREEN_HEIGHT"]))
    login = LoginScreen(window, net)
    login.run(clock)
    try:
        menu = Menu(window, net, player_id)
        opponent = None
    except pg.error:
        quit()

    while run:
        clock.tick(60)
        if not menu.both_ready() or opponent is None or opponent.heroes is None or player.heroes is None:
            try:
                player, opponent, which_map, menu.opponent_ready, potions, seed = net.send(["get_info", opponent_id])
                board = TiledMap(maps[str(which_map)], window)
            except (EOFError, TypeError, pg.error):
                break
            for event in pg.event.get():
                menu.highlight_buttons(event)
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
            if menu.player_ready:
                menu.waiting_screen()
        else:
            if not gui_start:
                create_potions(potions, player, opponent, board.object_tiles, net, seed)
                board.screen.fill((168, 139, 50))
                width = game_sets["GAME_SCREEN_WIDTH"] + box_sets["BOX_WIDTH"] * 2
                height = game_sets["GAME_SCREEN_HEIGHT"]
                window = pg.display.set_mode((width, height))
                gui = Gui(window, player, which_map, net)
                gui_start = True
            try:
                which_player_turn, turns = net.send(["get_turn", player_id])
            except TypeError:
                break
            try:
                actual_pos = pg.mouse.get_pos()
            except pg.error:
                break
            if opponent.last_action:
                player.react_to_event(opponent, net)
            gui.update_gui(actual_pos, player, opponent)
            player.check_result(opponent, net)
            move = redraw_window(window, board, player, opponent, which_player_turn, actual_pos, net, potions)
            try:
                end = net.send(["end", player.p_id])
            except EOFError:
                break
            if end:
                pg.time.delay(10000)
                pg.quit()
                run = False
            else:
                if move:
                    try:
                        net.send(["update", opponent_id])
                    except EOFError:
                        break
                for event in pg.event.get():
                    gui.click(event)
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()
                        break
                    if event.type == pg.MOUSEBUTTONUP and event.button == mouse_button["RIGHT"]:
                        player.clicked_hero = None
                    if event.type == pg.MOUSEBUTTONUP and event.button == mouse_button["LEFT"]:
                        if which_player_turn == player_id:

                            if not player.clicked_hero:
                                player.clicked_hero = player.check_clicked_hero(actual_pos)
                            else:
                                made_action = player.action(opponent, board.object_tiles, actual_pos, gui)
                                if made_action:
                                    net.send(made_action)
                                    player.clicked_hero = None
                    try:
                        gui.menu.react(event)
                    except pg.error:
                        break
                try:
                    opponent = net.send(["echo", opponent_id])
                except EOFError:
                    break


if __name__ == '__main__':
    main()
