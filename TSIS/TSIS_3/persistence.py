import json, os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"
DEFAULT_SETTINGS = {"sound": True, "car_color": "blue", "difficulty": "medium"}

def load_settings():
    try:
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS.copy()

def save_settings(s):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(s, f, indent=2)

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE) as f:
            return json.load(f)
    except:
        return []

def add_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": distance})
    lb.sort(key=lambda x: x["score"], reverse=True)
    lb = lb[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(lb, f, indent=2)
