import os, sys, json, shutil

def get_user_json():
    # Determine base path
    if getattr(sys, "frozen", False):
        base_path = os.path.join(os.path.expanduser("~"), ".hazometric")
    else:
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "save")

    os.makedirs(base_path, exist_ok=True)  # simpler check + creation

    user_json = os.path.join(base_path, "userData.json")

    # Ensure JSON exists
    if not os.path.exists(user_json):
        try:
            if getattr(sys, "_MEIPASS", False):
                # Copy default JSON from PyInstaller bundle
                default_json = os.path.join(sys._MEIPASS, "save", "userData.json")
                shutil.copy(default_json, user_json)
            else:
                # Normal Python: raise to fallback
                raise FileNotFoundError
        except Exception:
            # Fallback: create empty JSON
            with open(user_json, "w", encoding="utf-8") as f:
                json.dump({"games": {}, "settings": {"theme": "dark"}}, f, indent=4)

    return user_json
