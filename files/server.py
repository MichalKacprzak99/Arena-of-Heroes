import json
import socket
import pickle
import logging
import jsonpickle
from game import Game
from player import Player
from _thread import start_new_thread
from pymongo import MongoClient

fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)

id_count = 0
root = MongoClient("localhost", 27017)
aof_db = root['games_db']
games = aof_db['games']


class Server:
    def __init__(self):
        self.server = '127.0.0.1'
        self.port = 5556
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        self.s.listen()
        logger.info('Waiting for a connection, Server Started')

    def start(self):
        global id_count
        while True:
            conn, adr = self.s.accept()
            logger.info("Connected to: " + str(adr))
            id_count += 1
            player_id = 0
            if id_count % 2 == 1:
                game = Game()
                games.insert_one(json.loads(jsonpickle.encode(game)))
                logger.info("Creating a new game ...")
            else:
                player_id = 1
            start_new_thread(ThreadedClient().run, (conn, game, player_id))


class ThreadedClient:
    def __init__(self):
        self.reactions = {
            "get_info": self.get_info,
            "move": self.move,
            "basic_attack": self.attack,
            "special_attack": self.attack,
            "random_spell": self.random_spell,
            "heal": self.heal,
            "echo": self.echo,
            "is_ready": self.is_ready,
            "get_turn": self.get_turn,
            "update": self.update,
            "update_opponent": self.update_opponent,
            "reset_action": self.reset_action,
            "death_heroes": self.death_heroes,
            "result": self.result,
            "end": self.end,
            "save": self.save
        }
        self.reply = []
        self.data = []
        self.game = None

    def run(self, connection, game, p_id):
        global id_count
        game.players[p_id] = Player(name="df", player_id=p_id)
        connection.send(pickle.dumps(game.players[p_id]))
        self.game = game
        while True:
            if games.find_one({'time_start': self.game.time_start}):
                try:
                    self.data = pickle.loads(connection.recv(4096))
                    if not self.data:
                        break
                    else:
                        if self.data[0] in self.reactions:
                            self.reply = self.reactions[self.data[0]]()
                        logger.info("Received: " + str(self.data))
                        logger.info("Sending: " + str(self.reply))
                        connection.sendall(pickle.dumps(self.reply))
                        self.reply = None
                except EOFError:
                    break
            else:
                break
        logger.info("Lost connection")
        try:
            logger.info("Closing Game " + str(game.game_id))
            games.delete_one({'time_start': self.game.time_start})
        except KeyError:
            pass
        id_count -= 1
        connection.close()

    def get_info(self):
        opponent_ready = self.game.is_ready[abs(self.data[1] - 1)]
        return [self.game.players[self.data[1]], self.game.which_map, opponent_ready]

    def echo(self):
        return self.game.players[self.data[1]]

    def is_ready(self):
        self.game.is_ready[abs(self.data[1] - 1)] = self.data[2]
        return self.game.is_ready[self.data[1]]

    def get_turn(self):
        return [self.game.player_turn, self.game.turns]

    def end(self):
        if self.game.winner is not None and self.game.loser is not None:
            return True
        else:
            return False

    def death_heroes(self):
        self.game.players[self.data[1]].heroes = self.data[2]
        self.game.players[self.data[1]].death_heroes_pos = self.data[3]

    def reset_action(self):
        self.game.players[self.data[1]].last_action = None

    def update(self):
        self.game.players[self.data[1]].moved_hero = None

    def result(self):
        if self.data[2] == "lose":
            self.game.loser = self.data[1]
        elif self.data[2] == "win":
            self.game.winner = self.data[1]

    def update_opponent(self):
        self.game.players[abs(self.data[1] - 1)] = self.data[2]

    def random_spell(self):
        last_action = self.data[2]
        attacked_heroes = last_action[2]
        self.game.players[self.data[1]].last_action = last_action
        for attacked_hero in attacked_heroes:
            self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.get_next_turn()

    def attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.get_next_turn()

    def heal(self):
        hero_to_heal = self.data[2]
        self.game.players[self.data[1]].heroes[hero_to_heal.hero_id] = hero_to_heal
        self.game.get_next_turn()

    def move(self):
        moved_hero = self.data[2]
        self.game.players[self.data[1]].heroes[moved_hero.hero_id] = moved_hero
        self.game.players[self.data[1]].moved_hero = moved_hero
        self.game.get_next_turn()

    def save(self):
        version_to_save = json.loads(jsonpickle.encode(self.game))
        logger.info(games.find_one_and_replace({'time_start': self.game.time_start}, version_to_save))


if __name__ == '__main__':
    server = Server()
    server.start()
