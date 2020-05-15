
from pymongo import MongoClient

root = MongoClient("localhost", 27017)
aof_db = root['games_db']
games = aof_db['games']


# for game in games.find({}):
#     games.delete_one(game)

for game in games.find({}):
    print(game)
