import json
import socket
import pickle
import logging
import jsonpickle
import datetime
from game import Game
from player import Player
from _thread import start_new_thread
from pymongo import MongoClient
from itertools import islice

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
        self.port = 556
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
            start_new_thread(ThreadedClient().run, (conn, {"game": game}, player_id))


class ThreadedClient:
    def __init__(self):
        self.reactions = {
            "get_info": self.get_info,
            "is_ready": self.is_ready,
            "get_turn": self.get_turn,
            "result": self.result,
            "end": self.end,
            "save": self.save,
            "get_games_to_load": self.get_games_to_load,
            "load": self.load,
            "echo": self.echo,
            "update": self.update,
            "update_opponent": self.update_opponent,
            "reset_action": self.reset_action,
            "death_heroes": self.death_heroes,
            "move": self.move,
            "basic_attack": self.attack,
            "special_attack": self.attack,
            "random_spell": self.random_spell,
            "heal": self.heal
        }
        self.reply = []
        self.data = []
        self.game = None
        self.to_load = False
        self.p_id = None

    def run(self, connection, g, p_id):
        global id_count
        self.p_id = p_id
        self.game = g["game"]
        self.game.players[self.p_id] = Player(name="df", player_id=self.p_id)

        connection.send(pickle.dumps(self.p_id))

        while True:
            if games.find_one({'time_start': self.game.time_start}):
                if all(self.game.players) and self.game.add is False:
                    version_to_save = json.loads(jsonpickle.encode(self.game))
                    games.find_one_and_replace({'time_start': self.game.time_start}, version_to_save)
                    self.game.add = True
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
                        g["game"] = self.game
                        if self.data[0] == "end" and self.reply is True:
                            logger.info("End of Game ")
                            games.delete_one({'last_saved': self.game.last_saved})
                            break
                        self.reply = None
                except EOFError:
                    break
            else:
                break
        logger.info("Lost connection")
        try:
            logger.info("Closing Game ")
            logger.info("Delete")
            games.delete_many({'is_saved': False})
        except KeyError:
            pass
        id_count -= 1
        connection.close()

    def get_info(self):
        opponent_ready = self.game.is_ready[abs(self.data[1] - 1)]
        return [self.game.players[self.p_id], self.game.players[self.data[1]], self.game.which_map, opponent_ready]

    def is_ready(self):
        self.game.is_ready[abs(self.data[1] - 1)] = self.data[2]
        return self.game.is_ready[self.data[1]]

    def get_turn(self):
        return [self.game.player_turn, self.game.turns]

    def result(self):
        if self.data[2] == "lose":
            self.game.loser = self.data[1]
        elif self.data[2] == "win":
            self.game.winner = self.data[1]

    def end(self):
        return self.game.winner is not None and self.game.loser is not None

    def save(self):
        self.game.last_saved = datetime.datetime.now().strftime("%c")
        self.game.is_saved = True
        version_to_save = json.loads(jsonpickle.encode(self.game))
        games.find_one_and_replace({'time_start': self.game.time_start}, version_to_save)

    @staticmethod
    def get_games_to_load():
        find_games = games.find(filter={"last_saved": {"$ne": None}}, limit=2)
        real_game = []
        for find_game in find_games:
            sliced_game = dict(islice(find_game.items(), 1, len(find_game)))
            real_game.append(jsonpickle.decode(json.dumps(sliced_game)))
        return real_game

    def load(self):
        self.game.__dict__.update(self.data[1].__dict__)
        self.game.is_ready = [False, False]
        self.to_load = True

    def echo(self):
        return self.game.players[self.data[1]]

    def update(self):
        self.game.players[self.data[1]].moved_hero = None

    def update_opponent(self):
        self.game.players[abs(self.data[1] - 1)] = self.data[2]

    def death_heroes(self):
        self.game.players[self.data[1]].heroes = self.data[2]
        self.game.players[self.data[1]].death_heroes_pos = self.data[3]

    def reset_action(self):
        self.game.players[self.data[1]].last_action = None

    def move(self):
        moved_hero = self.data[2]
        self.game.players[self.data[1]].heroes[moved_hero.hero_id] = moved_hero
        self.game.players[self.data[1]].moved_hero = moved_hero
        self.game.get_next_turn()

    def attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.get_next_turn()

    def random_spell(self):
        last_action = self.data[2]
        attacked_heroes = last_action[2]
        self.game.players[self.data[1]].last_action = last_action
        for attacked_hero in attacked_heroes:
            self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.get_next_turn()

    def heal(self):
        hero_to_heal = self.data[2]
        self.game.players[self.data[1]].heroes[hero_to_heal.hero_id] = hero_to_heal
        self.game.get_next_turn()


if __name__ == '__main__':
    server = Server()
    server.start()
