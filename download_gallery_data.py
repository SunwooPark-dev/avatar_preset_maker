# download_gallery_data.py
import urllib.request
import json
import os

url = "https://reactorprompt.vercel.app/gallery-data.json"
output_file = "gallery-data.json"

print(f"Downloading from {url}...")
try:
    urllib.request.urlretrieve(url, output_file)
    size = os.path.getsize(output_file)
    print(f"Download complete! Size: {size / 1024:.2f} KB")
except Exception as e:
    print(f"Download failed: {e}")
    exit(1)

# Inspect the structure of the JSON file
try:
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Number of items in JSON: {len(data)}")
    if isinstance(data, list) and len(data) > 0:
        print("Sample item structure:")
        sample = data[0]
        for k, v in sample.items():
            val_str = str(v)
            if len(val_str) > 100:
                val_str = val_str[:100] + "..."
            print(f"  {k}: {val_str}")
except Exception as e:
    print(f"Parsing failed: {e}")
