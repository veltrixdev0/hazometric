from .readJSON import *
import json, os

def writeJSON(path, content, game_title):
    data = readJSON(path) # Read json

    data.setdefault("games", {}) # Ensure games exists
    data["games"][game_title] = content

    _saveJSON(path, data) # Save JSON

def removeJSON(path, game_title):
    data = readJSON(path)

    games = data.get("games", {})
    if game_title in games:
        del games[game_title]

    _saveJSON(path, data) # Save JSON

def addSetting(path, key, content):
    data = readJSON(path) # Read json

    data.setdefault("settings", {}) # Ensure settings exists
    data["settings"][key] = content

    _saveJSON(path,data)

def _saveJSON(path, data):
    try: # Try
        with open(path, "w", encoding="utf-8") as f: # Writes to JSON
            json.dump(data, f, indent=4) # Actually writes it
    except Exception as e: # Some exception, return error
        print(f"Failed to write JSON to {path}: {e}")