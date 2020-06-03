import json
import socket
import pickle
import logging
import jsonpickle
import datetime
from game import Game
from player import Player
from _thread import start_new_thread
from itertools import islice
from pymongo import MongoClient
import random
root = MongoClient("localhost", 27017)
aof_db = root['games_db']
games = aof_db['games']
users = aof_db['users']

fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)

id_count = 0


class Server:
    def __init__(self):
        self.server = '127.0.0.1'
        self.port = 8080
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        self.s.listen()
        logger.info('Waiting for a connection, Server Started')

    def start(self):
        global id_count
        seed = random.randint(0, 1000000)
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
            start_new_thread(ThreadedClient().run, (conn, {"game": game}, player_id, seed))


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
            "login": self.login,
            "sign up": self.sign_up,
            "basic_attack": self.attack,
            "special_attack": self.attack,
            "random_spell": self.random_spell,
            "heal": self.heal,
            "update_potions": self.update_potions
        }
        self.seed = 0
        self.reply = []
        self.data = []
        self.game = None
        self.to_load = False
        self.p_id = None

    def run(self, connection, g, p_id, seed):

        global id_count
        self.p_id = p_id
        self.game = g["game"]
        self.game.players[self.p_id] = Player(name="df", player_id=self.p_id)
        self.seed = seed
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
            self.log_out_user()
            logger.info("Closing Game ")
            logger.info("Delete")
            games.delete_many({'is_saved': False})
        except KeyError:
            pass
        id_count -= 1
        connection.close()

    def login(self):
        login_to_search = self.data[1]
        password_to_search = self.data[2]
        logger.info("SEARCHING FOR USER: " + login_to_search + " WITH PASSWORD: " + password_to_search)
        if users.find_one({"login": login_to_search, "password": password_to_search, "logged_in": 0}):
            post = {
                "login": login_to_search,
                "password": password_to_search,
                "logged_in": 1
            }
            self.game.players[self.p_id].name = login_to_search
            self.game.players[self.p_id].login = login_to_search
            users.find_one_and_replace({"login": login_to_search}, post)
            return True
        else:
            return False

    def sign_up(self):
        login_to_add = self.data[1]
        password_to_add = self.data[2]
        logger.info("ADDING USER: " + login_to_add + " WITH PASSWORD: " + password_to_add + "ID: " +
                    str(users.count_documents({}) + 1))
        if users.find_one({"login": login_to_add}):
            return False
        else:
            post = {
                "login": login_to_add,
                "password": password_to_add,
                "logged_in": 0
            }
            users.insert_one(post)
            return True

    def log_out_user(self):
        player_to_log_out = self.game.players[self.p_id]
        player_login_data = users.find_one({"login": player_to_log_out.login})
        post = {
            "login": player_login_data["login"],
            "password": player_login_data["password"],
            "logged_in": 0
        }
        users.find_one_and_replace({"login": player_login_data["login"]}, post)
        logger.info("LOGGING OUT USER WITH LOGIN: " + player_login_data["login"])

    def get_info(self):
        opponent_ready = self.game.is_ready[abs(self.data[1] - 1)]
        return [self.game.players[self.p_id], self.game.players[self.data[1]],
                self.game.which_map, opponent_ready, self.game.potions, self.seed]

    def is_ready(self):
        self.game.is_ready[abs(self.data[1] - 1)] = self.data[2]
        if len(self.data) > 3:
            self.game.players[self.data[1]].heroes = self.data[3]
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

    def get_games_to_load(self):
        name_of_player = self.game.players[self.p_id].name
        find_games = games.find(filter={"last_saved": {"$ne": None}, "players.name": name_of_player}, limit=2)
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

    def random_spell(self):
        last_action = self.data[2]
        attacked_heroes = last_action[2]
        self.game.players[self.data[1]].last_action = last_action
        for attacked_hero in attacked_heroes:
            self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.players[self.data[1]].special_attack = last_action[1]
        self.game.players[self.data[1]].attacked_with_special = attacked_heroes
        self.game.get_next_turn()

    def attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        attacking_hero = last_action[1]
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.players[self.data[1]].attacking_hero = attacking_hero
        self.game.players[self.data[1]].attacked_hero = attacked_hero
        self.game.get_next_turn()

    def special_attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        attacking_hero = last_action[1]
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.players[self.data[1]].special_attack = attacking_hero
        self.game.players[self.data[1]].attacked_with_special = attacked_hero
        self.game.get_next_turn()

    def heal(self):
        last_action = self.data[2]
        healing_hero = last_action[1]
        hero_to_heal = last_action[2]
        self.game.players[self.data[1]].special_attack = healing_hero
        self.game.players[self.data[1]].attacked_with_special = hero_to_heal
        self.game.players[self.data[1]].heroes[hero_to_heal.hero_id] = hero_to_heal
        self.game.get_next_turn()

    def update_potions(self):
        self.game.potions = self.data[1]
        if len(self.data) > 2:
            affected_hero = self.data[2]
            self.game.players[self.data[3]].heroes[affected_hero.hero_id] = affected_hero


if __name__ == '__main__':
    server = Server()
    server.start()
