import json
from enum import Enum

class Game (Enum):
    TRIVIA = "trivia_score"
    GEO = "geo_score"


def get_user_score(user_name : str, game_name : Game) -> int: 
    """Return the score of a player for a given game. Please use game enum from the import"""
    file = open("data/user_data.json",'r')
    data = json.load(file)
    file.close()
    if user_name in data.keys():
        return data[user_name][game_name.value]
    return 0
    
def increment_user_score(user_name : str, game_name : Game, points : int = 1):
    """Update the score of a user for a given game"""
    file = open("data/user_data.json",'r')
    data = json.load(file)
    file.close()
    if user_name not in data.keys():
        # This user doesn't exist. We create one
        data[user_name] = {"trivia_score" : 0, "geo_score" : 0, "incoming_chats" : []}
    data[user_name][game_name.value] += points
    file = open("data/user_data.json",'w')
    json.dump(data,file)
    file.close()

def get_user_data(user_name : str) -> dict : 
    file = open("data/user_data.json",'r')
    data = json.load(file)
    file.close()
    if user_name not in data.keys():
        # This user doesn't exist. We create one
        data[user_name] = {"trivia_score" : 0, "geo_score" : 0, "incoming_chats" : []}
        file = open("data/user_data.json",'w')
        json.dump(data,file)
        file.close()
    return data[user_name]


