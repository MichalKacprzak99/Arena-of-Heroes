from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np


def add_side(list_of_tiles):
    tmp = list_of_tiles[0]
    extended_list = []
    for tile in list_of_tiles[1:]:
        tmp_x, tmp_y = tmp
        if tmp_x < tile[0]:
            extended_list.append([tile, "east"])
        elif tmp_x > tile[0]:
            extended_list.append([tile, "west"])
        if tmp_y < tile[1]:
            extended_list.append([tile, "north"])
        elif tmp_y > tile[1]:
            extended_list.append([tile, "south"])
        tmp = tile
    return extended_list


def path_finder(player, opponent, object_tiles, new_pos):
    matrix = np.full((12, 12), 1)
    for hero in opponent.heroes:
        x, y = hero.pos
        matrix[y][x] = 0
    for tile in object_tiles:
        x, y = tile
        matrix[y][x] = 0
    for hero in player.heroes:
        if hero != player.moved_hero:
            x, y = hero.pos
            matrix[y][x] = 0
    grid = Grid(matrix=matrix)
    start = grid.node(player.moved_hero.pos[0], player.moved_hero.pos[1])
    end = grid.node(*new_pos)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)
    return add_side(path)


