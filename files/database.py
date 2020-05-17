import json
import jsonpickle
from bson import ObjectId
from pymongo import MongoClient
from itertools import islice
root = MongoClient("localhost", 27017)
aof_db = root['games_db']
games = aof_db['games']
# #
#
# for game in games.find({}):
#     games.delete_one(game)

# find_games = games.find(filter=None, limit=2)
#
# real_game = []
# for find_game in find_games:
#     sliced_game = dict(islice(find_game.items(), 1, len(find_game)))
#     print(sliced_game)
#     real_game.append(jsonpickle.decode(json.dumps(sliced_game)))
#
# for game in real_game:
#     print(game)
for game in games.find({}):
    print(game)
