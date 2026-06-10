import json
import os

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
status_path = os.path.join(WORK_DIR, "thumbnail_generation_status.json")

with open(status_path, "r", encoding="utf-8") as f:
    d = json.load(f)

keys = sorted([int(k) for k in d.keys()])
print(f"Total keys: {len(keys)}")
print(f"Min key: {keys[0]}, Max key: {keys[-1]}")
print("Keys list:")
print(keys)
