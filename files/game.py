from random import randint


class Game:
    def __init__(self, game_id):
        self.player_turn = 0
        self.turns = 0
        self.game_id = game_id
        self.players = [None, None]
        self.which_map = randint(0, 1)
        self.is_ready = [False, False]
