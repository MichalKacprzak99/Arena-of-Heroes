from settings import game_sets, box_sets, hero_images, colors, coordinate, load_image, get_tile_pos, tile_dim, result
import pygame as pg


def blit_text_center(screen, text_to_input, font, height, color):
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, color)
    width = game_sets["GAME_SCREEN_WIDTH"] + box_sets["BOX_WIDTH"] * 2
    screen.blit(text, (width / 2 - text_width / 2, height))


def draw_result_of_game(screen, player):
    if player.result is not None:
        result_image = pg.image.load(load_image(result[str(player.result)]))
        screen.blit(result_image, [350, 150])
    # blit_text_center(screen, text_to_input, font, 50, colors["RED"])


def draw_player_turn(screen, player_id, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Your turn" if player_id == player_turn else "Opponent's turn"
    blit_text_center(screen, text_to_input, font, 20, colors["RED"])


def highlight_tile(screen, board, player, opponent, pos):
    if box_sets["BOX_WIDTH"] < pos[0] < box_sets["RIGHT_BOX"]:
        color = colors["GREEN"]
        tmp_pos = get_tile_pos(pos)
        if player.clicked_hero and player.clicked_in_range(tmp_pos) is False:
            color = colors["GRAY"]
        if player.clicked_object(board.object_tiles,  tmp_pos):
            color = colors["BLACK"]
        if player.clicked_death_hero(tmp_pos) or opponent.clicked_death_hero(tmp_pos):
            color = colors["BLACK"]
        if player.clicked_opp_hero(opponent,  tmp_pos):
            color = colors["RED"]
        if player.clicked_own_hero(tmp_pos):
            color = colors["BLUE"]
        draw_pos = coordinate(tmp_pos)
        pg.draw.rect(screen, color, (*draw_pos, tile_dim["width"], tile_dim["height"]), 1)


def highlight_clicked_hero(screen, player):
    color = colors["BLUE"]
    draw_pos = coordinate(player.clicked_hero.pos)
    pg.draw.rect(screen, color, (*draw_pos, tile_dim["width"], tile_dim["height"]), 1)


def draw_health_bar(screen, hero, hero_coordinate):
    health_bar = (hero_coordinate[0] + 12, hero_coordinate[1])
    health_bar_width = 40 * float(hero.stats["HP"])
    health_bar_height = 5
    pg.draw.rect(screen, colors["RED"], (health_bar, (health_bar_width, health_bar_height)), 0)
    how_much_less_hp = 40 - health_bar_width
    if how_much_less_hp != 0:
        lose_hp = (health_bar[0] + health_bar_width, health_bar[1])
        pg.draw.rect(screen, colors["BLACK"], (lose_hp, (how_much_less_hp, 5)), 0)


def draw_hero(screen, hero, tile):
    hero_coordinate = coordinate(tile)
    hero_image = pg.image.load(load_image(hero_images[hero.stats["NAME"]][hero.side]))
    screen.blit(hero_image, hero_coordinate)
    draw_health_bar(screen, hero, hero_coordinate)


def draw_heroes(screen, player):
    for hero in player.heroes:
        if hero is not None:
            if hero is not player.moved_hero:
                draw_hero(screen, hero, hero.pos)

    for death_hero_pos in player.death_heroes_pos:
        if death_hero_pos is not None:
            draw_death_hero(screen, death_hero_pos, death_hero_pos.pos)


def draw_death_hero(screen, hero, tile):
    hero_coordinate = coordinate(tile)
    hero_image = pg.image.load(load_image(hero_images[hero.stats["NAME"]]["death"]))
    screen.blit(hero_image, hero_coordinate)


def draw_background(screen, board, player, opponent, player_turn, actual_pos):
    board.draw()
    highlight_tile(screen, board, player, opponent, actual_pos)
    draw_heroes(screen, player)
    draw_heroes(screen, opponent)
    draw_player_turn(screen, player.player_id, player_turn)
    draw_result_of_game(screen, player)
    if player.clicked_hero:
        highlight_clicked_hero(screen, player)


def draw_with_moving_hero(screen, board, player, opponent, player_turn, actual_pos, tile):
    draw_background(screen, board, player, opponent, player_turn, actual_pos)
    draw_hero(screen, player.moved_hero, tile)
    pg.display.update()
    pg.time.delay(500)


def redraw_window(screen, board, player, opponent, player_turn, actual_pos, n):
    made_move = False
    if player.moved_hero:
        for tile, side in player.moved_hero.path:
            player.moved_hero.side = side
            draw_with_moving_hero(screen, board, player, opponent, player_turn, actual_pos, tile)
        player.heroes[player.moved_hero.hero_id].side = player.moved_hero.side
        player.moved_hero = None
    if opponent.moved_hero:
        for tile, side in opponent.moved_hero.path:
            opponent.moved_hero.side = side
            draw_with_moving_hero(screen, board, opponent, player, player_turn, actual_pos, tile)
        opponent.heroes[opponent.moved_hero.hero_id].side = opponent.moved_hero.side
        opponent.moved_hero = None
        n.send(["update_opponent", player.player_id, opponent])
        made_move = True
    else:
        draw_background(screen, board, player, opponent, player_turn, actual_pos)
        pg.display.update()
    return made_move
