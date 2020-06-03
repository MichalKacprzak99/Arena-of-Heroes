from settings import game_settings, box_settings, hero_images, colors, coordinate, load_image, get_tile_pos, tile_dim
import pygame as pg


def blit_text_center(screen, text_to_input, font, height, color):
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, color)
    width = game_settings["GAME_SCREEN_WIDTH"] + box_settings["BOX_WIDTH"] * 2
    screen.blit(text, (width / 2 - text_width / 2, height))


def draw_result_of_game(screen, player):
    font = pg.font.SysFont("Arial", 50)
    text_to_input = player.result
    blit_text_center(screen, text_to_input, font, 50, colors["RED"])


def draw_player_turn(screen, player_id, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Your turn" if player_id == player_turn else "Opponent's turn"
    blit_text_center(screen, text_to_input, font, 20, colors["RED"])


def highlight_tile(screen, board, player, opponent, pos):
    if box_settings["BOX_WIDTH"] < pos[0] < box_settings["RIGHT_BOX"]:
        color = colors["GREEN"]
        tmp_pos = get_tile_pos(pos)
        if player.clicked_hero and player.clicked_in_range(tmp_pos) is False:
            color = colors["GRAY"]
        if player.clicked_object(board.object_tiles, tmp_pos):
            color = colors["BLACK"]
        if player.clicked_death_hero(tmp_pos) or opponent.clicked_death_hero(tmp_pos):
            color = colors["BLACK"]
        if player.clicked_opp_hero(opponent, tmp_pos):
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


def draw_attacking_hero_animation(screen, hero, tile, frame_counter, total_frames, type_of_attack):
    current_image_counter = total_frames - frame_counter

    if type_of_attack == "basic" or type_of_attack == "special_hit":
        if current_image_counter < 10:
            current_hero_image = hero_images[hero.stats["NAME"]]["attacking"][hero.side] + \
                                 "0" + str(current_image_counter) + ".png"
        else:
            current_hero_image = hero_images[hero.stats["NAME"]]["attacking"][hero.side] + \
                                 str(current_image_counter) + ".png"
    elif type_of_attack == "special":
        if current_image_counter < 10:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_attack"] + \
                                 str(current_image_counter) + ".png"
        else:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_attack"] + \
                                 str(current_image_counter) + ".png"
    # elif type_of_attack == "special_hit":
    #     if current_image_counter < 10:
    #         current_hero_image = hero_images[hero.stats["NAME"]]["special_hit"] + \
    #                              str(current_image_counter) + ".png"
    #     else:
    #         current_hero_image = hero_images[hero.stats["NAME"]]["special_hit"] + \
    #                              str(current_image_counter) + ".png"
    elif type_of_attack == "special_shoot":
        if current_image_counter < 10:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_shoot"] + \
                                 str(current_image_counter) + ".png"
        else:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_shoot"] + \
                                 str(current_image_counter) + ".png"
    elif type_of_attack == "special_opponents":
        if current_image_counter < 10:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_lightning"] + \
                                 str(current_image_counter) + ".png"
        else:
            current_hero_image = hero_images[hero.stats["NAME"]]["special_lightning"] + \
                                 str(current_image_counter) + ".png"

    hero_image = pg.image.load(load_image(current_hero_image))
    tile_coordinates = coordinate(tile)
    screen.blit(hero_image, tile_coordinates)
    draw_health_bar(screen, hero, tile_coordinates)


def draw_heroes(screen, player):
    # heroes_not_to_draw = []
    # if player.special_attack:
    #     for heroes in player.attacked_with_special: # zmienic na przypisywanie z player.heroes[hero_id]
    #         heroes_not_to_draw.append(heroes)
    # if player.attacking_hero:
    #     heroes_not_to_draw.append(player.attacking_hero)
    # if player.moved_hero:
    #     heroes_not_to_draw.append(player.moved_hero)
    #
    # for hero in player.heroes:
    #     if hero is not None:
    #         # if hero is not player.moved_hero and hero is not player.attacking_hero:
    #         if hero not in heroes_not_to_draw:
    #             draw_hero(screen, hero, hero.pos)

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
    draw_player_turn(screen, player.player_id, player_turn)
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
    animation_counter, total_frames = 0, 0
    opp_animation_counter, opp_total_frames = 0, 0

    if player.special_attack:
        if player.special_attack.stats["NAME"] == "MAGE":
            animation_counter, total_frames = 4, 4
            opp_animation_counter, opp_total_frames = 8, 8
        elif player.special_attack.stats["NAME"] == "HEALER":
            animation_counter, total_frames = 6, 6
        elif player.special_attack.stats["NAME"] == "WARRIOR":
            animation_counter, total_frames = 6, 6
        elif player.special_attack.stats["NAME"] == "ARCHER":
            animation_counter, total_frames = 6, 6

    if player.attacking_hero:
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
        if player.attacking_hero:
            which_attack = "basic"
            draw_attacking_hero_animation(screen, player.attacking_hero, actual_pos, animation_counter, total_frames,
                                          which_attack)
        else:
            which_attack = "special"
            if player.special_attack.stats["NAME"] == "HEALER":
                draw_attacking_hero_animation(screen, player.special_attack, player.attacked_with_special.pos,
                                              animation_counter, total_frames, which_attack)
            elif player.special_attack.stats["NAME"] == "WARRIOR":
                which_attack = "special_hit"
                draw_attacking_hero_animation(screen, player.special_attack, actual_pos, animation_counter,
                                              total_frames, which_attack)
                pg.time.delay(30)
            elif player.special_attack.stats["NAME"] == "ARCHER":
                which_attack = "special_shoot"
                draw_attacking_hero_animation(screen, player.special_attack, player.attacked_with_special.pos,
                                              animation_counter, total_frames, which_attack)
                pg.time.delay(30)
            elif player.special_attack.stats["NAME"] == "MAGE":
                draw_attacking_hero_animation(screen, player.special_attack, actual_pos, animation_counter,
                                              total_frames, which_attack)
                pg.time.delay(30)
                which_attack = "special_opponents"
                for heroes in player.attacked_with_special:
                    draw_attacking_hero_animation(screen, heroes, heroes.pos, opp_animation_counter,
                                                  opp_total_frames, which_attack)
                    pg.time.delay(20)
            else:
                draw_attacking_hero_animation(screen, player.special_attack, actual_pos, animation_counter,
                                              total_frames, which_attack)
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
        n.send(["update_opponent", player.player_id, opponent])
        made_move = True
    if player.special_attack:
        if player.special_attack.stats["NAME"] == "WARRIOR" or player.special_attack.stats["NAME"] == "HEALER":
            if player.attacked_with_special.pos[0] > player.special_attack.pos[0]:
                player.special_attack.side = "east"
            if player.attacked_with_special.pos[0] < player.special_attack.pos[0]:
                player.special_attack.side = "west"
            if player.attacked_with_special.pos[1] > player.special_attack.pos[1]:
                player.special_attack.side = "south"
            if player.attacked_with_special.pos[1] < player.special_attack.pos[1]:
                player.special_attack.side = "north"
        player.heroes[player.special_attack.hero_id].side = player.special_attack.side
        draw_attacking_hero(screen, board, player, opponent, player_turn, player.special_attack.pos)
        player.special_attack = None
        player.attacked_with_special = None
    if opponent.special_attack:
        if opponent.special_attack.stats["NAME"] == "WARRIOR" or opponent.special_attack.stats["NAME"] == "HEALER":
            if opponent.attacked_with_special.pos[0] > opponent.special_attack.pos[0]:
                opponent.special_attack.side = "east"
            if opponent.attacked_with_special.pos[0] < opponent.special_attack.pos[0]:
                opponent.special_attack.side = "west"
            if opponent.attacked_with_special.pos[1] > opponent.special_attack.pos[1]:
                opponent.special_attack.side = "south"
            if opponent.attacked_with_special.pos[1] < opponent.special_attack.pos[1]:
                opponent.special_attack.side = "north"
        opponent.heroes[opponent.special_attack.hero_id].side = opponent.special_attack.side
        draw_attacking_hero(screen, board, opponent, player, player_turn, opponent.special_attack.pos)
        opponent.special_attack = None
        opponent.attacked_with_special = None
        n.send(["update_opponent", player.player_id, opponent])
    if player.attacking_hero:
        if player.attacked_hero.pos[0] > player.attacking_hero.pos[0]:
            player.attacking_hero.side = "east"
        if player.attacked_hero.pos[0] < player.attacking_hero.pos[0]:
            player.attacking_hero.side = "west"
        if player.attacked_hero.pos[1] > player.attacking_hero.pos[1]:
            player.attacking_hero.side = "south"
        if player.attacked_hero.pos[1] < player.attacking_hero.pos[1]:
            player.attacking_hero.side = "north"
        player.heroes[player.attacking_hero.hero_id].side = player.attacking_hero.side
        draw_attacking_hero(screen, board, player, opponent, player_turn, player.attacking_hero.pos)
        player.attacking_hero = None
    if opponent.attacking_hero:
        if opponent.attacked_hero.pos[0] > opponent.attacking_hero.pos[0]:
            opponent.attacking_hero.side = "east"
        if opponent.attacked_hero.pos[0] < opponent.attacking_hero.pos[0]:
            opponent.attacking_hero.side = "west"
        if opponent.attacked_hero.pos[1] > opponent.attacking_hero.pos[1]:
            opponent.attacking_hero.side = "south"
        if opponent.attacked_hero.pos[1] < opponent.attacking_hero.pos[1]:
            opponent.attacking_hero.side = "north"
        opponent.heroes[opponent.attacking_hero.hero_id].side = opponent.attacking_hero.side
        draw_attacking_hero(screen, board, opponent, player, player_turn, opponent.attacking_hero.pos)
        opponent.attacking_hero = None
        n.send(["update_opponent", player.player_id, opponent])
        made_move = True
    else:
        draw_background(screen, board, player, opponent, player_turn, actual_pos)
        pg.display.update()
    return made_move
