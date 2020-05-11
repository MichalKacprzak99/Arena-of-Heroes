from random import randint


class Game:
    def __init__(self, game_id):
        self.player_turn = 0
        self.turns = 0
        self.game_id = game_id
        self.players = [None, None]
        self.which_map = randint(0, 4)
        self.is_ready = [False, False]
        self.winner = None
        self.loser = None

    def get_next_turn(self):
        self.player_turn = abs(self.player_turn - 1)
        self.turns += 1
