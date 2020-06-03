import socket
import pickle
from game import Game
from player import Player
from _thread import start_new_thread
import logging

fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)

id_count = 0


class Server:
    def __init__(self):
        self.server = '127.0.0.1'
        self.port = 5556
        self.games = {}
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
            game_id = (id_count - 1) // 2
            if id_count % 2 == 1:
                self.games[game_id] = Game(game_id)
                logger.info("Creating a new game ...")
            else:
                player_id = 1
            start_new_thread(ThreadedClient().run, (conn, self.games, player_id, game_id))


class ThreadedClient:
    def __init__(self):
        self.reactions = {
            "get_info": self.get_info,
            "move": self.move,
            "basic_attack": self.attack,
            # "special_attack": self.attack,
            "special_attack": self.special_attack,
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
            "end": self.end
        }
        self.reply = []
        self.data = []
        self.game = None

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
        self.game.players[self.data[1]].special_attack = last_action[1]  # animation special
        self.game.players[self.data[1]].attacked_with_special = attacked_heroes  # animation special
        self.game.get_next_turn()

    def attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        attacking_hero = last_action[1] # animation
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.players[self.data[1]].attacking_hero = attacking_hero  # animation
        self.game.players[self.data[1]].attacked_hero = attacked_hero  # animation
        self.game.get_next_turn()

    def special_attack(self):
        last_action = self.data[2]
        attacked_hero = last_action[2]
        attacking_hero = last_action[1]
        self.game.players[self.data[1]].last_action = last_action
        self.game.players[abs(self.data[1] - 1)].heroes[attacked_hero.hero_id] = attacked_hero
        self.game.players[self.data[1]].special_attack = attacking_hero  # animation special
        self.game.players[self.data[1]].attacked_with_special = attacked_hero  # animation special
        self.game.get_next_turn()

    def heal(self):
        last_action = self.data[2]
        healing_hero = last_action[1]
        hero_to_heal = last_action[2]
        self.game.players[self.data[1]].special_attack = healing_hero  # animation special
        self.game.players[self.data[1]].attacked_with_special = hero_to_heal  # animation special
        self.game.players[self.data[1]].heroes[hero_to_heal.hero_id] = hero_to_heal
        self.game.get_next_turn()

    def move(self):
        moved_hero = self.data[2]
        self.game.players[self.data[1]].heroes[moved_hero.hero_id] = moved_hero
        self.game.players[self.data[1]].moved_hero = moved_hero
        self.game.get_next_turn()

    def run(self, connection, games, p_id, g_id):
        global id_count
        games[g_id].players[p_id] = Player(name="df", player_id=p_id)
        connection.send(pickle.dumps(games[g_id].players[p_id]))
        while True:
            try:
                self.data = pickle.loads(connection.recv(4096))

                if g_id in games:
                    self.game = games[g_id]
                    if not self.data:
                        break
                    else:
                        if self.data[0] in self.reactions:
                            self.reply = self.reactions[self.data[0]]()
                        logger.info("Received: " + str(self.data))
                        logger.info("Sending: " + str(self.reply))
                        connection.sendall(pickle.dumps(self.reply))
                        self.reply = None
                else:
                    break
            except EOFError:
                break
        logger.info("Lost connection")
        try:
            del games[g_id]
            logger.info("Closing Game " + str(g_id))
        except KeyError:
            pass
        id_count -= 1
        connection.close()


if __name__ == '__main__':
    server = Server()
    server.start()
