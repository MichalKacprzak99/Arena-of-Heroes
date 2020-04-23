from files.player import Player


class Game:
    def __init__(self, game_id):
        self.player_turn = 0
        self.turns = 0
        self.game_id = game_id
        self.players = [Player(player_id=0), Player(player_id=1)]
        self.ready = False
