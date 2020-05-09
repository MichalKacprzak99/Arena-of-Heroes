import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import game_settings, box_settings, client_name, maps, mouse_button
from drawing import redraw_window
from menu import Menu
from gui import Gui

pg.init()
pg.font.init()


def react_to_event(player, opponent):
    name_of_action = opponent.last_action[0]
    if opponent.last_action[0] == "basic_attack":
        attacking_hero = opponent.last_action[1]
        attacked_hero = opponent.last_action[2]
        attacked_hero.stats["HP"] -= attacking_hero.stats["ATTACK"] - attacked_hero.stats["DEFENSE"] / 2
        player.heroes[attacked_hero.hero_id] = attacked_hero
    if opponent.last_action[0] == "bolt":
        attacking_hero = opponent.last_action[1]
        attacked_hero = opponent.last_action[2]
        attacked_hero.stats["HP"] -= attacking_hero.stats["ATTACK"]
        player.heroes[attacked_hero.hero_id] = attacked_hero
    opponent.last_action = None

def main():
    run = True
    gui_start = False
    clock = pg.time.Clock()
    n = Network()
    player = n.get_player()
    player_id = player.player_id
    pg.display.set_caption(client_name[str(player_id)])
    print(("Hi, you are client: "+str(player_id)))
    opponent_id = abs(player_id - 1)
    window = pg.display.set_mode((game_settings["GAME_SCREEN_WIDTH"], game_settings["GAME_SCREEN_HEIGHT"]))
    menu = Menu(window)

    while run:
        clock.tick(60)
        if not menu.both_ready():
            try:
                opponent, which_map, menu.opponent_ready = n.send(["get_info", opponent_id])
                board = TiledMap(maps[str(which_map)], window)
            except EOFError:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONUP:
                    actual_pos = pg.mouse.get_pos()
                    menu.click(actual_pos, n, player_id)
            if menu.player_ready:
                menu.loading_screen()
        else:
            if not gui_start:
                board.screen.fill((168, 139, 50))
                width = game_settings["GAME_SCREEN_WIDTH"] + box_settings["BOX_WIDTH"] * 2
                height = game_settings["GAME_SCREEN_HEIGHT"]
                window = pg.display.set_mode((width, height))

                gui = Gui(window, player_id)
                gui_start = True
            try:
                which_player_turn, turns = n.send("get_turn")
            except EOFError:
                break
            actual_pos = pg.mouse.get_pos()
            if opponent.last_action:
                react_to_event(player, opponent)
            gui.update_gui(actual_pos, player, opponent)
            move = redraw_window(window, board, player, opponent, which_player_turn, actual_pos)
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
                        if not player.clicked_hero:
                            player.check_clicked_hero(actual_pos)
                        else:
                            made_action = player.action(opponent, board.object_tiles, actual_pos, gui)
                            if made_action:
                                n.send(made_action)
                gui.menu.react(event)
            try:
                opponent = n.send(["echo", opponent_id])
            except EOFError:
                break


if __name__ == '__main__':
    main()
