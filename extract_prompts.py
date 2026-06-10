# extract_prompts.py
import urllib.request
import re
import json

url = "https://reactorprompt.vercel.app/assets/index-xeFgVNeB.js"
output_js = "reactor_js.js"

print("Downloading JS bundle...")
try:
    urllib.request.urlretrieve(url, output_js)
    print("Download completed.")
except Exception as e:
    print(f"Download failed: {e}")
    exit(1)

print("Reading JS file...")
with open(output_js, "r", encoding="utf-8") as f:
    content = f.read()

print(f"JS length: {len(content)} characters")

# Let's search for patterns in the JS file.
# We'll look for strings containing keywords like 'prompt', 'category' or some known titles like '시네마틱 스튜디오'.
# Let's search for the prompts data list.
# A common pattern for hardcoded react arrays: [{id:"...",title:"...",category:"...",prompt:"..."}]
# Let's find some characters that look like prompt items.
# Let's look for Korean keywords in the file since the website has titles/descriptions in Korean.
# We can search for all occurrences of unicode or Korean characters.
korean_words = re.findall(r'[\uac00-\ud7a3]+', content)
print(f"Found {len(korean_words)} Korean words. Sample: {korean_words[:20]}")

# Let's search for arrays or object properties.
# Since we know the prompt website has categories like '인물', '코스프레', '음식', '일러스트' 등.
# Let's look for these categories inside the JS.
# Reactor Prompts has specific prompts. We can search for patterns.
# Let's write a regex that matches JSON-like objects in the JS file.
# E.g., {..., prompt:"...", ...}
# Let's try to find potential prompt objects.
# We can find all matches of things like prompt: "..." or prompt: '...'
prompt_matches = re.findall(r'prompt:\s*["\']([^"\']+)["\']', content)
print(f"Found {len(prompt_matches)} raw prompt matches.")

# Let's extract items that contain titles, categories, and prompts.
# Let's inspect a slice of the JS file that contains Korean words to see how the data is structured.
# Let's find where the Korean characters start.
first_ko_idx = content.find("인물")
if first_ko_idx != -1:
    print(f"Found '인물' at index {first_ko_idx}. Surrounding content:")
    print(content[max(0, first_ko_idx - 500): min(len(content), first_ko_idx + 1500)])
else:
    # try searching other categories
    for cat in ["코스프레", "음식", "일러스트", "갤러리"]:
        idx = content.find(cat)
        if idx != -1:
            print(f"Found '{cat}' at index {idx}. Surrounding content:")
            print(content[max(0, idx - 500): min(len(content), idx + 1500)])
            break
