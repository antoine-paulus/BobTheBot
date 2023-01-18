import json
from enum import Enum

class Game (Enum):
    TRIVIA = "trivia_score"
    GEO = "geo_score"


def get_user_score(user_name : str, game_name : Game) -> int: 
    """Return the score of a player for a given game. Please use game enum from the import"""
    data = _get_data_from_json()
    if user_name in data.keys():
        return data[user_name][game_name.value]
    return 0


def increment_user_score(user_name : str, game_name : Game, points : int = 1):
    """Update the score of a user for a given game"""
    data = _get_data_from_json()
    if user_name not in data.keys():
        # This user doesn't exist. We create one
        data[user_name] = {"trivia_score" : 0, "geo_score" : 0, "incoming_chats" : []}
    data[user_name][game_name.value] += points
    _write_data_on_json(data)


def get_user_data(user_name : str) -> dict : 
    data = _get_data_from_json()
    if user_name not in data.keys():
        # This user doesn't exist. We create one
        data[user_name] = {"trivia_score" : 0, "geo_score" : 0, "incoming_chats" : []}
        _write_data_on_json(data)
    return data[user_name]


def get_user_messages(user_name : str) -> list : 
    """Get chat messages for a given user"""
    data = _get_data_from_json()
    if user_name not in data.keys():
        return []
    else : 
        return data[user_name]["incoming_chats"]


def delete_user_messages(user_name : str):
    """Delete all messeages sent to a given user"""
    data = _get_data_from_json()
    if user_name in data.keys():
        data[user_name]["incoming_chats"] = []
    _write_data_on_json(data)


def send_user_message(sender_name : str, receiver_name : str, message : str):
    """Send a message to a given user"""
    data = _get_data_from_json()
    if receiver_name not in data.keys():
        # This user doesn't exist. We create one
        data[receiver_name] = {"trivia_score" : 0, "geo_score" : 0, "incoming_chats" : []}
    data[receiver_name]["incoming_chats"].append({"from" : sender_name, "content" : message})
    _write_data_on_json(data)

def user_in_database(user_name : str) -> bool : 
    """return if a user is in database"""
    data = _get_data_from_json()
    return user_name in data.keys()

def _get_data_from_json() -> dict:
    """Return the content of the json database"""
    file = open("data/user_data.json",'r')
    data = json.load(file)
    file.close()
    return data

def _write_data_on_json(data : dict) : 
    """Re-write the json database from the data passed in parameters"""
    file = open("data/user_data.json",'w')
    json.dump(data,file)
    file.close()

if __name__ == "__main__" : 
    print(get_user_score('jane',Game.GEO))
    print(increment_user_score('jane',Game.GEO,5))
    print(get_user_score('jane',Game.GEO))
    print(get_user_messages('jane'))
    print(send_user_message('Antoine','jane','Hi Jane, this is a test.'))
    print(get_user_messages('jane'))
    print(delete_user_messages('jane'))
    print(get_user_messages('jane'))