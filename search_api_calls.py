# search_api_calls.py
import re

output_js = "reactor_js.js"

with open(output_js, "r", encoding="utf-8") as f:
    content = f.read()

# Search for fetch calls
fetch_matches = re.findall(r'fetch\([^)]+\)', content)
print(f"Fetch matches found: {fetch_matches[:10]}")

# Search for supabase or firebase or vercel API URLs
api_urls = re.findall(r'https?://[^\s"\']+', content)
# filter for potential API hosts (exclude fonts, google, reactjs, vercel, etc.)
exclude_hosts = ['fonts.', 'google.', 'w3.org', 'react.dev', 'reactjs.', 'vitejs.']
filtered_urls = [url for url in api_urls if not any(eh in url for eh in exclude_hosts)]
print(f"API or external URLs found: {set(filtered_urls)}")
