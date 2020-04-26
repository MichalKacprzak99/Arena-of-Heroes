import socket
from _thread import *
import sys
from game import Game
from player import Player
from hero import Hero
import pickle
#server = "10.10.0.102"
server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)#the number of maximum connected clients
print("Waiting for a connection, Server Started")
games = {}
idCount = 0


def threaded_client(conn, player,gameId):
    global idCount
    games[gameId].players[player] = Player(name="df", player_id=p)
    conn.send(pickle.dumps(games[gameId].players[player]))
    reply = []

    while True:
        try:
            data = pickle.loads(conn.recv(2048))  # lista [attack, id postaci atakujacej, ta co obrywa, za ile , arg*]

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    which_player_take_action = data[1]
                    if data[0] == "get_another_player":
                        reply = [game.players[which_player_take_action], game.ready]
                    if data[0] == "move":
                        moved_hero = data[2]
                        game.players[which_player_take_action].heroes[moved_hero.hero_id] = moved_hero
                        game.player_turn = abs(game.player_turn - 1)
                        game.turns += 1
                        reply = game.players[which_player_take_action]
                    if data[0] == "echo":
                        reply = game.players[which_player_take_action]
                    if data == "get_turn":
                        reply = [game.player_turn, game.turns]

                    print("receivved: ", data)
                    print("Sending: ", reply)
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)

        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))