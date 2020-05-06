import pygame as pg
from network import Network
from tile_map import TiledMap
from settings import GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, BOX_WIDTH, CLIENT_NAME, MAPS
from drawing import redraw_window
from gui import Gui
import thorpy



pg.init()
window = pg.display.set_mode((GAME_SCREEN_WIDTH + BOX_WIDTH*2, GAME_SCREEN_HEIGHT))
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
    game_start = False
    stored_event = None
    while run:
        clock.tick(60)
        if game_start is False:
            try:
                opponent, game_start, which_map = n.send(["get_info", opponent_id])
                gui = Gui(window)
                board = TiledMap(MAPS[str(which_map)], window)
            except EOFError:
                break
        else:
            try:
                which_player_turn, turns = n.send("get_turn")
            except EOFError:
                break
            actual_pos = pg.mouse.get_pos()

            gui.update_gui(actual_pos, player, opponent)
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
                            feedback = player.action(opponent, board.not_valid_tiles, actual_pos)
                            if feedback:
                                n.send(feedback)

            try:
                opponent = n.send(["echo", opponent_id])
            except EOFError:
                break


if __name__ == '__main__':
    main()
