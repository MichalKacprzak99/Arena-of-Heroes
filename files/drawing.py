from settings import WIDTH, HEIGHT, HERO_IMAGES, COLORS, coordinate, load_image, get_tile_pos
import pygame as pg


def draw_player_turn(screen, player_turn):
    font = pg.font.SysFont("Arial", 25)
    text_to_input = "Player %d turn" % player_turn
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, COLORS["RED"])
    screen.blit(text, (WIDTH/2 - text_width/2, 20))


def highlight_tile(screen, board, player, opponent, pos):
    color = COLORS["GREEN"]
    if pos in board.not_valid_tiles:
        color = COLORS["BLACK"]
    if any(map(lambda opp_hero: pos == opp_hero.pos, opponent.heroes)):
        color = COLORS["RED"]
    if any(map(lambda hero: pos == hero.pos, player.heroes)):
        color = COLORS["BLUE"]
    drawing_pos = coordinate(pos)
    pg.draw.rect(screen, color, (drawing_pos[0], drawing_pos[1], 64, 64), 1)


def draw_if_clicked(screen):
    font = pg.font.SysFont("Arial", 15)
    text_to_input = "Clicked"
    text_width, text_height = font.size(text_to_input)
    text = font.render(text_to_input, True, COLORS["RED"])
    screen.blit(text, (WIDTH/2 - text_width/2, 50))


def draw_heroes(screen, player):
    for hero in player.heroes:
        hero_image = pg.image.load(load_image(HERO_IMAGES[str(hero.image_id)]))
        screen.blit(hero_image, coordinate(hero.pos))


def redraw_window(screen, board, player, opponent, player_turn, clicked_hero, actual_pos):
    board.draw()
    highlight_tile(screen, board, player, opponent, get_tile_pos(actual_pos))
    draw_heroes(screen, player)
    draw_heroes(screen, opponent)
    draw_player_turn(screen, player_turn)
    if clicked_hero is not None:
        draw_if_clicked(screen)
    pg.display.update()
