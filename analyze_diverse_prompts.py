import json
import os

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
gallery_path = os.path.join(WORK_DIR, "gallery-data.json")

with open(gallery_path, "r", encoding="utf-8") as f:
    data = json.load(f)

posts = data.get("posts", [])
diverse_posts = [p for p in posts if p.get("id") and 90000 <= p.get("id") <= 90150]

output_txt = os.path.join(WORK_DIR, "diverse_prompts_list.txt")
with open(output_txt, "w", encoding="utf-8") as out:
    out.write(f"Total diverse posts: {len(diverse_posts)}\n\n")
    for p in diverse_posts:
        out.write(f"ID: {p['id']} | Caption: {p['caption']}\n")
        out.write(f"Tags: {p.get('tags', [])}\n")
        out.write(f"Prompt: {p['prompt']}\n")
        out.write("=" * 80 + "\n\n")

print(f"Dumped {len(diverse_posts)} posts to {output_txt}")

