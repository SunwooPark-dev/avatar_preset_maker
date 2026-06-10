#!/usr/bin/env python3
"""Check available Gemini image models and OpenAI gpt-image-1 correct params."""
import os
import json
import urllib.request
import urllib.error

def clean_key(k):
    return (k or "").lstrip("\ufeff").strip()

GEMINI_KEY = clean_key(os.environ.get("GEMINI_API_KEY",""))
OPENAI_KEY = clean_key(os.environ.get("OPENAI_API_KEY",""))

print("=== Gemini: List models with 'image' in name ===")
if GEMINI_KEY:
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            data = json.loads(r.read())
        models = data.get("models", [])
        image_models = [m for m in models if "image" in m.get("name","").lower() or "imagen" in m.get("name","").lower()]
        for m in image_models:
            print(f"  {m['name']} | methods: {m.get('supportedGenerationMethods',[])}")
        if not image_models:
            print("  No image models found. Showing all flash models:")
            for m in models:
                if "flash" in m.get("name","").lower():
                    print(f"  {m['name']} | {m.get('supportedGenerationMethods',[])}")
    except Exception as e:
        print(f"  Error: {e}")
else:
    print("  No GEMINI_API_KEY")

print()
print("=== OpenAI: Test gpt-image-1 without response_format ===")
if OPENAI_KEY:
    body = json.dumps({
        "model": "gpt-image-1",
        "prompt": "A simple red circle on white background",
        "n": 1,
        "size": "1024x1024"
        # No response_format - let server default
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Content-Type":"application/json","Authorization":f"Bearer {OPENAI_KEY}"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read())
        d0 = data.get("data",[{}])[0]
        has_url = bool(d0.get("url"))
        has_b64 = bool(d0.get("b64_json"))
        print(f"  SUCCESS! has_url={has_url} has_b64={has_b64}")
        if has_url:
            print(f"  URL prefix: {d0['url'][:60]}...")
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()
        err_obj = json.loads(body_err) if body_err else {}
        print(f"  HTTP {e.code}: {err_obj.get('error',{}).get('message','')[:200]}")
        print(f"  Code: {err_obj.get('error',{}).get('code','')}")
    except Exception as e:
        print(f"  Error: {e}")
else:
    print("  No OPENAI_API_KEY")
