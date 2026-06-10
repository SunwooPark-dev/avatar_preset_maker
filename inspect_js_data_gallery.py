# inspect_js_data_gallery.py
import re
import json

output_js = "reactor_js.js"

with open(output_js, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for category words: category:"portrait" or category:"illustration" or category:"photo"
# Let's find occurrences of category:"portrait" or category:"character" or category:"illustration"
# Note that in minified JS, key might not have quotes: category:"portrait" or category:"illustration"
matches = list(re.finditer(r'category:\s*["\'](portrait|illustration|photo|character|cosplay|watercolor|cyberpunk)["\']', content))
print(f"Found {len(matches)} occurrences of categories.")

# Let's see some matches around the index
for i, m in enumerate(matches[:5]):
    start = max(0, m.start() - 200)
    end = min(len(content), m.end() + 500)
    print(f"--- Match {i} at {m.start()} ---")
    print(content[start:end])

# Let's see if there is a massive list of posts.
# Let's search for "posts" or similar names, or a very long array in the code.
# Usually, a react app might have a data file import or inline array: `const posts = [...]` or `const DATA = [...]`
# Let's search for "posts" or "galleryData" or "items"
# We can search for strings containing "--v 6.0" or "--ar" or other Midjourney syntax which would be in the actual gallery prompts.
mj_matches = list(re.finditer(r'--v\s+\d+(\.\d+)?', content))
print(f"Found {len(mj_matches)} occurrences of Midjourney '--v' parameters.")
if mj_matches:
    print("Sample Midjourney prompt surroundings:")
    for i, m in enumerate(mj_matches[:3]):
        print(f"--- MJ Match {i} at {m.start()} ---")
        print(content[max(0, m.start() - 300): min(len(content), m.end() + 300)])
