from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np


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
    return path[1:-1]


