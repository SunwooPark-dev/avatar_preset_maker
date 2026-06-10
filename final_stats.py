import os, json

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY_DIR = os.path.join(WORK_DIR, "gallery-images")
STATUS_FILE = os.path.join(WORK_DIR, "thumbnail_generation_status.json")

# Image file stats
pngs = [f for f in os.listdir(GALLERY_DIR) if f.endswith(".png")]
total_bytes = sum(os.path.getsize(os.path.join(GALLERY_DIR, f)) for f in pngs)
print(f"Gallery images: {len(pngs)} files, {total_bytes/1024/1024:.1f} MB")

# Status breakdown
with open(STATUS_FILE, "r", encoding="utf-8") as f:
    status = json.load(f)

success = sum(1 for v in status.values() if v.get("status") == "success")
failed  = sum(1 for v in status.values() if v.get("status") == "failed")
print(f"Status: {success} success / {failed} failed / {len(status)} total records")

# Show failed if any
if failed:
    print("\nFailed posts:")
    for pid, v in status.items():
        if v.get("status") == "failed":
            print(f"  Post {pid}")
