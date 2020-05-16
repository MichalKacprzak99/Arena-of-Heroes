from random import randint
import datetime


class Game:
    def __init__(self):
        self.time_start = datetime.datetime.now().strftime("%c")
        self.last_saved = None
        self.player_turn = 0
        self.turns = 0
        self.players = [None, None]
        self.which_map = randint(0, 3)
        self.is_ready = [False, False]
        self.winner = None
        self.loser = None

    def get_next_turn(self):
        self.player_turn = abs(self.player_turn - 1)
        self.turns += 1

    def __repr__(self):
        description = "The game is between {0} and {1}.\nStarted: {3}.\n Last saved:"\
            .format(self.players[0].name, self.players[0].name, self.time_start, self.last_saved)
        return description
