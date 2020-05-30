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
    hp_bar = (hero_coordinate[0] + 12, hero_coordinate[1])
    hp_bar_width = 40 * float(hero.stats["HP"])
    hp_bar_height = 5
    pg.draw.rect(screen, colors["RED"], (hp_bar, (hp_bar_width, hp_bar_height)), 0)
    less_hp = 40 - hp_bar_width
    if less_hp != 0:
        cords = hp_bar[0] + hp_bar_width, hp_bar[1]
        pg.draw.rect(screen, colors["BLACK"], (cords, (less_hp, hp_bar_height)), 0)


def draw_hero(screen, hero, tile):
    hero_coordinate = coordinate(tile)
    hero_image = pg.image.load(load_image(hero_images[hero.stats["NAME"]][hero.side]))
    screen.blit(hero_image, hero_coordinate)
    draw_health_bar(screen, hero, hero_coordinate)


def draw_animated_hero(screen, hero, tile, frame_counter, total_frames):
    current_image_counter = total_frames - frame_counter
    if current_image_counter < 10:
        current_hero_image = hero_images[hero.stats["NAME"]]["walking"][hero.side] + \
                             "0" + str(current_image_counter) + ".png"
    else:
        current_hero_image = hero_images[hero.stats["NAME"]]["walking"][hero.side] + \
                             str(current_image_counter) + ".png"

    hero_image = pg.image.load(load_image(current_hero_image))
    tile_coordinates = coordinate(tile)
    if hero.side == "east":
        hero_coordinate = [tile_coordinates[0] - int((frame_counter * (64 / (total_frames + 1)))), tile_coordinates[1]]
    elif hero.side == "west":
        hero_coordinate = [tile_coordinates[0] + int((frame_counter * (64 / (total_frames + 1)))), tile_coordinates[1]]
    elif hero.side == "south":
        hero_coordinate = [tile_coordinates[0], tile_coordinates[1] - int((frame_counter * (64 / (total_frames + 1))))]
    else:
        hero_coordinate = [tile_coordinates[0], tile_coordinates[1] + int((frame_counter * (64 / (total_frames + 1))))]

    screen.blit(hero_image, hero_coordinate)
    draw_health_bar(screen, hero, hero_coordinate)


def draw_attacking_hero_animation(screen, hero, tile, frame_counter, total_frames):
    current_image_counter = total_frames - frame_counter
    if current_image_counter < 10:
        current_hero_image = hero_images[hero.stats["NAME"]]["attacking"][hero.side] + \
                             "0" + str(current_image_counter) + ".png"
    else:
        current_hero_image = hero_images[hero.stats["NAME"]]["attacking"][hero.side] + \
                             str(current_image_counter) + ".png"
    hero_image = pg.image.load(load_image(current_hero_image))
    tile_coordinates = coordinate(tile)
    screen.blit(hero_image, tile_coordinates)
    draw_health_bar(screen, hero, tile_coordinates)


def draw_heroes(screen, player):
    for hero in player.heroes:
        if hero is not None:
            if hero is not player.moved_hero and hero is not player.attacking_hero:
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
    draw_player_turn(screen, player.p_id, player_turn)
    draw_result_of_game(screen, player)
    if player.clicked_hero:
        highlight_clicked_hero(screen, player)


def draw_with_animation_hero(screen, board, player, opponent, player_turn, actual_pos, tile):
    mage = False
    if player.moved_hero.stats["NAME"] == "MAGE":
        animation_counter, total_frames = 17, 17
        mage = True
    else:
        animation_counter, total_frames = 29, 29
    while animation_counter >= 0:
        draw_background(screen, board, player, opponent, player_turn, actual_pos)
        draw_animated_hero(screen, player.moved_hero, tile, animation_counter, total_frames)
        pg.display.update()
        if mage:
            pg.time.delay(30)
        else:
            pg.time.delay(15)
        animation_counter -= 1
    pg.display.update()


def draw_attacking_hero(screen, board, player, opponent, player_turn, actual_pos):
    mage = False
    healer = False
    if player.attacking_hero.stats["NAME"] == "MAGE":
        animation_counter, total_frames = 8, 8
        mage = True
    elif player.attacking_hero.stats["NAME"] == "HEALER":
        animation_counter, total_frames = 29, 29
        healer = True
    else:
        animation_counter, total_frames = 14, 14
    while animation_counter >= 0:
        draw_background(screen, board, player, opponent, player_turn, actual_pos)
        draw_attacking_hero_animation(screen, player.attacking_hero, actual_pos, animation_counter, total_frames)
        pg.display.update()
        if mage:
            pg.time.delay(30)
        elif healer:
            pg.time.delay(10)
        else:
            pg.time.delay(20)
        animation_counter -= 1
    pg.display.update()


def redraw_window(screen, board, player, opponent, player_turn, actual_pos, n):
    made_move = False
    if player.moved_hero:
        for tile, side in player.moved_hero.path:
            player.moved_hero.side = side
            draw_with_animation_hero(screen, board, player, opponent, player_turn, actual_pos, tile)
        player.heroes[player.moved_hero.hero_id].side = player.moved_hero.side
        player.moved_hero = None
    if opponent.moved_hero:
        for tile, side in opponent.moved_hero.path:
            opponent.moved_hero.side = side
            draw_with_animation_hero(screen, board, opponent, player, player_turn, actual_pos, tile)
        opponent.heroes[opponent.moved_hero.hero_id].side = opponent.moved_hero.side
        opponent.moved_hero = None
        n.send(["update_opponent", player.p_id, opponent])
        made_move = True
    if player.attacking_hero:
        if player.attacked_hero.pos[0] > player.attacking_hero.pos[0]:
            player.heroes[player.attacking_hero.hero_id].side = "east"
        if player.attacked_hero.pos[0] < player.attacking_hero.pos[0]:
            player.heroes[player.attacking_hero.hero_id].side = "west"
        if player.attacked_hero.pos[1] > player.attacking_hero.pos[1]:
            player.heroes[player.attacking_hero.hero_id].side = "south"
        if player.attacked_hero.pos[1] < player.attacking_hero.pos[1]:
            player.heroes[player.attacking_hero.hero_id].side = "north"
        draw_attacking_hero(screen, board, player, opponent, player_turn, player.attacking_hero.pos)
        player.attacking_hero = None
    else:
        draw_background(screen, board, player, opponent, player_turn, actual_pos)
        pg.display.update()
    return made_move
