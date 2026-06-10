import json
import os

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")

def main():
    if not os.path.exists(GALLERY_DATA):
        print("Error: gallery-data.json not found")
        return

    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    print(f"Original total posts: {len(posts)}")

    # Split diverse posts (id >= 90000) and other posts
    diverse_posts = [p for p in posts if p.get("id", 0) >= 90000]
    other_posts = [p for p in posts if p.get("id", 0) < 90000]

    print(f"Diverse posts count: {len(diverse_posts)}")
    print(f"Other posts count: {len(other_posts)}")

    # Move diverse posts to the front
    new_posts = diverse_posts + other_posts

    data["posts"] = new_posts

    with open(GALLERY_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Successfully reordered gallery-data.json. Diverse posts are now at the front.")

if __name__ == "__main__":
    main()
