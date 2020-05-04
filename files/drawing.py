from settings import WIDTH, HEIGHT, HERO_IMAGES, COLORS, coordinate, load_image, get_tile_pos
import pygame as pg
from player import Player


def draw_player_turn(screen, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Player %d turn" % player_turn
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, COLORS["RED"])
    screen.blit(text, (WIDTH/2 - text_width/2, 20))


def highlight_tile(screen, board, player, opponent,  pos):
    color = COLORS["GREEN"]
    if player.clicked_hero is not None and player.clicked_in_range(pos) is False:
        color = COLORS["GRAY"]
    if player.clicked_object(board.object_tiles, pos):
        color = COLORS["BLACK"]
    if player.clicked_opponent_hero(opponent, pos):
        color = COLORS["RED"]
    if player.clicked_own_hero(pos):
        color = COLORS["BLUE"]
    drawing_pos = coordinate(pos)
    pg.draw.rect(screen, color, (drawing_pos[0], drawing_pos[1], 64, 64), 1)


def draw_if_clicked(screen):
    font = pg.font.SysFont("Arial", 15)
    text_to_input = "Clicked"
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, COLORS["RED"])
    screen.blit(text, (WIDTH/2 - text_width/2, 50))


def draw_health_bar(screen, hero, hero_coordinate):
    health_bar = (hero_coordinate[0] + 12, hero_coordinate[1])
    health_bar_width = 40 * hero.health // 100
    health_bar_height = 5
    pg.draw.rect(screen, COLORS["RED"], (health_bar, (health_bar_width, health_bar_height)), 0)
    how_much_less_hp = 40 - health_bar_width
    if how_much_less_hp != 0:
        lose_hp = (health_bar[0] + health_bar_width, health_bar[1])
        pg.draw.rect(screen, COLORS["BLACK"], (lose_hp, (how_much_less_hp, 5)), 0)


def draw_heroes(screen, player):
    for hero in player.heroes:
        if hero is not player.moved_hero:
            hero_coordinate = coordinate(hero.pos)
            hero_image = pg.image.load(load_image(HERO_IMAGES[str(hero.image_id)]))
            screen.blit(hero_image, hero_coordinate)
            draw_health_bar(screen, hero, hero_coordinate)


def draw_moved_hero(screen, player, tile):
    hero = player.moved_hero
    hero_coordinate = coordinate(tile)
    hero_image = pg.image.load(load_image(HERO_IMAGES[str(hero.image_id)]))
    screen.blit(hero_image, hero_coordinate)
    draw_health_bar(screen, hero, hero_coordinate)


def draw_background(screen, board, player, opponent, player_turn, clicked_hero, actual_pos):
    board.draw()
    highlight_tile(screen, board, player, opponent, get_tile_pos(actual_pos))
    draw_heroes(screen, player)
    draw_heroes(screen, opponent)
    draw_player_turn(screen, player_turn)
    if clicked_hero is not None:
        draw_if_clicked(screen)


def draw_all(screen, board, player, opponent, player_turn, clicked_hero, actual_pos, tile):
    draw_background(screen, board, player, opponent, player_turn, clicked_hero, actual_pos)
    draw_moved_hero(screen, player, tile)
    pg.display.update()
    pg.time.delay(500)


def redraw_window(screen, board, player, opponent, player_turn, clicked_hero, actual_pos):
    make_move = False
    if player.moved_hero is None or opponent.moved_hero is None:
        draw_background(screen, board, player, opponent, player_turn, clicked_hero, actual_pos)
        pg.display.update()
    if player.moved_hero:
        for tile in player.list_of_tiles:
            draw_all(screen, board, player, opponent, player_turn, clicked_hero, actual_pos, tile)
        player.moved_hero = None
    if opponent.moved_hero:
        for tile in opponent.list_of_tiles:
            draw_all(screen, board, opponent, player, player_turn, clicked_hero, actual_pos, tile)
        make_move = True
        return make_move

    return make_move

