from .readJSON import *
import json


def writeJSON(path, content, game_title):
    data = readJSON(path)

    # Make sure "games" key exists
    if "games" not in data:
        data["games"] = {}

    # Add or update the game
    data["games"][game_title] = content

    # Save back to file
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def removeJSON(path, game_title):
    data = readJSON(path)

    # Make sure "games" key exists
    if "games" not in data:
        data["games"] = {}

    # Remove the game
    if game_title in data["games"]:
        del data["games"][game_title]

    # Save back to file
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
