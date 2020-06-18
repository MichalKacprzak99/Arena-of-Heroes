from settings import game_sets, box_sets, hero_images, potion_img,\
    colors, coordinate, load_image, get_tile_pos, tile_dim, result, index_error_handler
import pygame as pg


def blit_text_center(screen, text_to_input, font, height, color):
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, color)
    width = game_sets["GAME_SCREEN_WIDTH"] + box_sets["BOX_WIDTH"] * 2
    screen.blit(text, (width / 2 - text_width / 2, height))


def draw_result_of_game(screen, player):
    result_image = pg.image.load(load_image(result[str(len(player.heroes))]))
    screen.blit(result_image, [350, 150])
    pg.display.update()


def check_hero_side(attacked, attacking):
    side = attacking.side
    if attacked.pos[0] > attacking.pos[0]:
        side = "east"
    if attacked.pos[0] < attacking.pos[0]:
        side = "west"
    if attacked.pos[1] > attacking.pos[1]:
        side = "south"
    if attacked.pos[1] < attacking.pos[1]:
        side = "north"
    return side


def draw_player_turn(screen, p_id, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Your turn" if p_id == player_turn else "Opponent's turn"
    blit_text_center(screen, text_to_input, font, 20, colors["RED"])


def highlight_tile(screen, board, player, opponent, pos):
    if box_sets["BOX_WIDTH"] < pos[0] < box_sets["RIGHT_BOX"]:
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
    movement = int((frame_counter * (64 / (total_frames + 1))))

    if hero.side == "east":
        hero_coordinate = [tile_coordinates[0] - movement, tile_coordinates[1]]
    elif hero.side == "west":
        hero_coordinate = [tile_coordinates[0] + movement, tile_coordinates[1]]
    elif hero.side == "south":
        hero_coordinate = [tile_coordinates[0], tile_coordinates[1] - movement]
    else:
        hero_coordinate = [tile_coordinates[0], tile_coordinates[1] + movement]
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
    else:
        if current_image_counter < 10:
            current_hero_image = hero_images[hero.stats["NAME"]][type_of_attack] + \
                                 str(current_image_counter) + ".png"
        else:
            current_hero_image = hero_images[hero.stats["NAME"]][type_of_attack] + \
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


def draw_potions(screen, potions):
    for potion in potions:
        potion_coordinate = coordinate(potion.pos)
        potion_image = pg.image.load(load_image(potion_img[potion.name]))
        screen.blit(potion_image, potion_coordinate)


def draw_background(screen, board, player, opponent, player_turn, actual_pos, potions):
    board.draw()
    highlight_tile(screen, board, player, opponent, actual_pos)
    draw_heroes(screen, player)
    draw_heroes(screen, opponent)
    draw_player_turn(screen, player.p_id, player_turn)
    # draw_result_of_game(screen, player)
    draw_potions(screen, potions)
    if player.clicked_hero:
        highlight_clicked_hero(screen, player)


def draw_with_animation_hero(screen, board, player, opponent, player_turn, actual_pos, tile, potions):
    mage = False
    if player.moved_hero.stats["NAME"] == "MAGE":
        animation_counter, total_frames = 17, 17
        mage = True
    else:
        animation_counter, total_frames = 29, 29
    while animation_counter >= 0:
        draw_background(screen, board, player, opponent, player_turn, actual_pos, potions)
        draw_animated_hero(screen, player.moved_hero, tile, animation_counter, total_frames)
        pg.display.update()
        if mage:
            pg.time.delay(30)
        else:
            pg.time.delay(15)
        animation_counter -= 1
    pg.display.update()


def draw_attacking_hero(screen, board, player, opponent, player_turn, actual_pos, potions):
    mage = False
    healer = False
    animation_counter, total_frames = 0, 0
    opp_animation_counter, opp_total_frames = 0, 0

    if player.special_attack:
        if player.special_attack.stats["NAME"] == "MAGE":
            animation_counter, total_frames = 4, 4
            opp_animation_counter, opp_total_frames = 8, 8
        else:
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
        draw_background(screen, board, player, opponent, player_turn, actual_pos, potions)
        if player.attacking_hero:
            which_attack = "basic"
            draw_attacking_hero_animation(screen, player.attacking_hero, actual_pos, animation_counter, total_frames,
                                          which_attack)
        else:
            which_attack = "special_attack"
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
                which_attack = "special_lightning"
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


@index_error_handler
def check_if_reach_potion(potions, tile):
    return list(filter(lambda potion: tile == potion.pos, potions))[0]


def react_to_potion(potions, tile, player, net):
    potion = check_if_reach_potion(potions, tile)
    if potion:
        potion.affect(player.moved_hero)
        del potions[potions.index(potion)]
        net.send(["update_potions", potions, player.moved_hero, player.p_id])


def redraw_window(screen, board, player, opponent, player_turn, actual_pos, n, potions):
    made_move = False

    def moved(p1, p2):
        for tile, face_to in p1.moved_hero.path:
            p1.moved_hero.side = face_to
            react_to_potion(potions, tile, p1, n)
            draw_with_animation_hero(screen, board, p1, p2, player_turn, actual_pos, tile, potions)
        p1.heroes[p1.moved_hero.hero_id].side = p1.moved_hero.side
        p1.moved_hero = None

    if player.moved_hero:
        moved(player, opponent)
    if opponent.moved_hero:
        moved(opponent, player)
        n.send(["update_opponent", player.p_id, opponent])
        made_move = True

    def special_attack(p1, p2):
        if p1.special_attack.stats["NAME"] != "MAGE":
            p1.heroes[p1.special_attack.hero_id].side = check_hero_side(p1.attacked_with_special, p1.special_attack)
        draw_attacking_hero(screen, board, p1, p2, player_turn, p1.special_attack.pos, potions)
        p1.special_attack = None
        p1.attacked_with_special = None

    if player.special_attack:
        special_attack(player, opponent)
    if opponent.special_attack:
        special_attack(opponent, player)
        n.send(["update_opponent", player.p_id, opponent])

    def attack(p1, p2):
        p1.heroes[p1.attacking_hero.hero_id].side = check_hero_side(p1.attacked_hero, p1.attacking_hero)
        draw_attacking_hero(screen, board, p1, p2, player_turn, p1.attacking_hero.pos, potions)
        p1.attacking_hero = None

    if player.attacking_hero:
        attack(player, opponent)
    if opponent.attacking_hero:
        attack(opponent, player)
        n.send(["update_opponent", player.p_id, opponent])
        made_move = True
    else:
        draw_background(screen, board, player, opponent, player_turn, actual_pos, potions)
        pg.display.update()
    return made_move
