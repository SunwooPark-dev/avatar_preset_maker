import json, os
from collections import Counter

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
with open(os.path.join(WORK_DIR, "gallery-data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

posts = data.get("posts", [])

CATEGORIES = ['portrait','illustration','product','food','character',
              'plush','poster','sticker','photo','infographic','design','other']

# Category distribution
posts_by_cat = {}
for p in posts:
    tags = p.get('tags', ['other'])
    cat = tags[0] if tags else 'other'
    if cat not in CATEGORIES: cat = 'other'
    posts_by_cat.setdefault(cat, []).append(p)

print("=== Current Category Distribution ===")
for cat in CATEGORIES:
    ps = posts_by_cat.get(cat, [])
    print(f"  {cat:15s}: {len(ps):3d} posts")

print(f"\nTotal: {len(posts)} posts")

# Sample prompts from each category (top 3)
print("\n=== Sample Prompts by Category (first 3) ===")
for cat in CATEGORIES:
    ps = posts_by_cat.get(cat, [])[:3]
    print(f"\n[{cat}]")
    for p in ps:
        prompt = (p.get('prompt','') or '')[:120]
        caption = (p.get('caption','') or '').replace('\n',' ')[:50]
        print(f"  Caption: {caption}")
        print(f"  Prompt:  {prompt}...")
        print()
