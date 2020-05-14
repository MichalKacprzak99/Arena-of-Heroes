import socket
import pickle
from game import Game
from player import Player
from _thread import start_new_thread
import logging

server = ''
port = 5556

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()

fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)
logger.info('Waiting for a connection, Server Started')

games = {}
id_count = 0


def threaded_client(connection, p_id, g_id):
    global id_count
    games[g_id].players[p_id] = Player(name="df", player_id=p_id)
    connection.send(pickle.dumps(games[g_id].players[p_id]))
    reply = []

    while True:
        try:
            data = pickle.loads(connection.recv(4096))

            if g_id in games:
                game = games[g_id]

                if not data:
                    break
                else:
                    which_player_take_action = data[1]
                    if data[0] == "get_info":
                        opponent_ready = game.is_ready[abs(which_player_take_action-1)]
                        reply = [game.players[which_player_take_action], game.which_map, opponent_ready]
                    if data[0] == "move":
                        moved_hero = data[2]
                        game.players[which_player_take_action].heroes[moved_hero.hero_id] = moved_hero
                        game.players[which_player_take_action].moved_hero = moved_hero
                        game.get_next_turn()
                    if data[0] == "basic_attack" or data[0] == "special_attack":
                        last_action = data[2]
                        attacked_hero = last_action[2]
                        game.players[which_player_take_action].last_action = last_action
                        game.players[abs(which_player_take_action-1)].heroes[attacked_hero.hero_id] = attacked_hero
                        game.get_next_turn()
                    if data[0] == "random_spell":
                        last_action = data[2]
                        attacked_heroes = last_action[2]
                        game.players[which_player_take_action].last_action = last_action
                        for attacked_hero in attacked_heroes:
                            game.players[abs(which_player_take_action - 1)].heroes[
                                attacked_hero.hero_id] = attacked_hero
                        game.get_next_turn()
                    if data[0] == "heal":
                        hero_to_heal = data[2]
                        game.players[which_player_take_action].heroes[hero_to_heal.hero_id] = hero_to_heal
                        game.get_next_turn()
                    if data[0] == "echo":
                        reply = game.players[which_player_take_action]
                    if data[0] == "is_ready":
                        game.is_ready[abs(which_player_take_action-1)] = data[2]
                        reply = game.is_ready[which_player_take_action]
                    if data == "get_turn":
                        reply = [game.player_turn, game.turns]
                    if data[0] == "update_opponent":
                        game.players[abs(which_player_take_action-1)] = data[2]
                    if data[0] == "update":
                        game.players[which_player_take_action].moved_hero = None
                    if data[0] == "reset_action":
                        game.players[which_player_take_action].last_action = None
                    if data[0] == "death_heroes":
                        game.players[which_player_take_action].heroes = data[2]
                        game.players[which_player_take_action].death_heroes_pos = data[3]
                    if data[0] == "result":
                        if data[2] == "lose":
                            game.loser = data[1]
                        elif data[2] == "win":
                            game.winner = data[1]
                    if data[0] == "end":
                        if game.winner is not None and game.loser is not None:
                            reply = True
                        else:
                            reply = False

                    logger.info("Received: " + str(data))
                    logger.info("Sending: " + str(reply))
                    connection.sendall(pickle.dumps(reply))
                    reply = None
            else:
                break
        except EOFError:
            break

    logger.info("Lost connection")
    try:
        del games[game_id]
        logger.info("Closing Game " + str(game_id))
    except KeyError:
        pass
    id_count -= 1
    connection.close()


player_id = 0
if __name__ == '__main__':
    while True:
        conn, adr = s.accept()
        logger.info("Connected to: " + str(adr))
        id_count += 1
        player_id = 0
        game_id = (id_count - 1) // 2
        if id_count % 2 == 1:
            games[game_id] = Game(game_id)

            logger.info("Creating a new game ...")
        else:
            player_id = 1

        start_new_thread(threaded_client, (conn, player_id, game_id))
