import json, os

def readJSON(path):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"Failed to decode from JSON file: {path}")