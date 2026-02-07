import json, os

def readJSON(path):
    # Checks if path exists
    if not os.path.exists(path):
        print(f"JSON file not found: {path}")
        return {}

    # Try to read JSON
    try:
        with open(path, 'r', encoding="utf-8") as file: # Open File
            return json.load(file) # Return the loaded JSON file
    except json.JSONDecodeError: # Error in decode
        print(f"Failed to decode from JSON file: {path}")
        return {}
    except Exception as e: # Any exception, then return the error.
        print(f"Error reading JSON file {path}: {e}")
        return {}