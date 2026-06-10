# find_js_chunks.py
import re

output_js = "reactor_js.js"

with open(output_js, "r", encoding="utf-8") as f:
    content = f.read()

# Search for patterns like assets/something.js or "something.js" or import("./...")
# E.g., re.findall(r'assets/[\w-]+\.js', content)
js_assets = re.findall(r'assets/[\w-]+\.js', content)
print(f"JS assets found: {set(js_assets)}")

# Also look for dynamic import paths
dynamic_imports = re.findall(r'["\']\./([\w-]+)\.js["\']', content)
print(f"Dynamic imports found: {set(dynamic_imports)}")

# Also look for any string ending in .js in quotes
js_strings = re.findall(r'["\']/assets/([\w-]+)\.js["\']', content)
print(f"JS strings found: {set(js_strings)}")
