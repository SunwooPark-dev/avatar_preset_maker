# inspect_js_data.py
import re
import json

output_js = "reactor_js.js"

with open(output_js, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for keywords that might represent fields in the prompt items
# e.g., "title", "prompt", "category", "tags", "images"
# Let's search for occurrences of these strings as property names in JS (like `title:` or `category:`)
# Since it might be minified, it could be `a:"title"` or something, or it might be raw JSON embedded as a string, or simple JS object literals.
# Let's search for some typical keywords or find all double-quoted strings.
# Reactor prompt website shows prompts. Let's look for common prompt words in English: "photorealistic", "cinematic", "highly detailed", "illustration", "masterpiece".
# Let's see if we can find "photorealistic" in the JS.
idx = content.lower().find("photorealistic")
if idx != -1:
    print(f"Found 'photorealistic' at index {idx}. Surrounding:")
    print(content[max(0, idx - 300): min(len(content), idx + 1000)])
else:
    print("Could not find 'photorealistic'")

# Let's search for "masterpiece"
idx_mp = content.lower().find("masterpiece")
if idx_mp != -1:
    print(f"Found 'masterpiece' at index {idx_mp}. Surrounding:")
    print(content[max(0, idx_mp - 300): min(len(content), idx_mp + 1000)])

# Let's search for common Midjourney prompt markers like "--v 6" or "--ar" or "--style raw"
idx_mj = content.lower().find("--v ")
if idx_mj != -1:
    print(f"Found '--v ' at index {idx_mj}. Surrounding:")
    print(content[max(0, idx_mj - 300): min(len(content), idx_mj + 1000)])
else:
    idx_mj2 = content.lower().find("--ar")
    if idx_mj2 != -1:
        print(f"Found '--ar' at index {idx_mj2}. Surrounding:")
        print(content[max(0, idx_mj2 - 300): min(len(content), idx_mj2 + 1000)])
