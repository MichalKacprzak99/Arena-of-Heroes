from random import randint


class Game:
    def __init__(self, game_id):
        self.player_turn = 0
        self.turns = 0
        self.game_id = game_id
        self.players = [None, None]
        self.ready = False
        self.which_map = randint(0, 0)
