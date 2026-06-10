#!/usr/bin/env python3
"""
generate_thumbnails_direct.py  v3
- OpenAI 완전 제거 (billing_hard_limit_reached)
- Primary:   gemini-2.5-flash-image (generateContent, 빠름)
- Fallback:  gemini-3.1-flash-image-preview (generateContent)
- Fallback2: imagen-4.0-fast-generate-001 (predict API)
- Prompt refinement: gemini-2.5-flash (text, 무료 쿼터)
"""
import os, json, base64, time, re, sys, argparse
import urllib.request, urllib.error

WORK_DIR        = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
STATUS_FILE     = os.path.join(WORK_DIR, "thumbnail_generation_status.json")
GALLERY_DATA    = os.path.join(WORK_DIR, "gallery-data.json")
GALLERY_IMAGES_DIR = os.path.join(WORK_DIR, "gallery-images")
LOGS_DIR        = os.path.join(WORK_DIR, "logs")

CATEGORIES = [
    'portrait','illustration','product','food','character',
    'plush','poster','sticker','photo','infographic','design','other'
]

def clean_key(k):
    return (k or "").lstrip("\ufeff").strip()

GEMINI_KEY = clean_key(os.environ.get("GEMINI_API_KEY",""))

# ─── HTTP ────────────────────────────────────────────────────────────────────
def post_json(url, headers, body, timeout=90):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req  = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:400]}"
    except Exception as e:
        return None, str(e)

def gemini_generate_content(model_id, contents, gen_cfg=None, timeout=90):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model_id}:generateContent?key={GEMINI_KEY}")
    body = {"contents": contents}
    if gen_cfg:
        body["generationConfig"] = gen_cfg
    return post_json(url, {"Content-Type":"application/json"}, body, timeout)

def imagen_predict(model_id, prompt, timeout=90):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{model_id}:predict?key={GEMINI_KEY}")
    body = {
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1}
    }
    return post_json(url, {"Content-Type":"application/json"}, body, timeout)

# ─── Status ──────────────────────────────────────────────────────────────────
def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_status(s):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)

# ─── Prompt Refinement (Gemini text) ─────────────────────────────────────────
REFINE_MODEL = "gemini-2.5-flash"

def refine_prompt(prompt, caption, category):
    if not GEMINI_KEY:
        return prompt
    system = (
        "You are an expert image generation prompt engineer. "
        "Rewrite the given prompt to be detailed, vivid, and entirely in English. "
        "Fill in bracketed placeholders like [CHARACTER], [인물], [배경색] with concrete, "
        "visually rich examples suitable for a style library thumbnail. "
        "Translate Korean to English. Expand short prompts into full descriptive sentences. "
        "Output ONLY the refined English prompt. No explanation, no intro, no markdown."
    )
    user = f"Category: {category}\nCaption: {caption}\nPrompt: {prompt}"
    contents = [
        {"role": "user", "parts": [
            {"text": system + "\n\n" + user}
        ]}
    ]
    resp, err = gemini_generate_content(REFINE_MODEL, contents, timeout=30)
    if err:
        print(f"  [Refine⚠️ ] {err[:100]}")
        return prompt
    try:
        refined = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
        refined = re.sub(r'^[\"\'`]+|[\"\'`]+$', '', refined).strip()
        return refined if refined else prompt
    except Exception as e:
        print(f"  [Refine⚠️ ] Parse: {e}")
        return prompt

# ─── Image Generation ─────────────────────────────────────────────────────────
def _extract_image_from_gemini_resp(resp):
    """gemini generateContent 응답에서 이미지 bytes 추출."""
    try:
        for part in resp["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                return base64.b64decode(part["inlineData"]["data"]), None
        return None, "No inlineData in response parts"
    except Exception as e:
        return None, f"Parse error: {e}"

def try_gemini_flash_image(prompt, model_id):
    """gemini-*-image via generateContent."""
    contents = [{"role":"user","parts":[{"text": prompt}]}]
    gen_cfg  = {"responseModalities": ["Text","Image"]}
    resp, err = gemini_generate_content(model_id, contents, gen_cfg, timeout=120)
    if err:
        return None, err
    img_bytes, e2 = _extract_image_from_gemini_resp(resp)
    return img_bytes, e2

def try_imagen(prompt, model_id):
    """imagen-4.0-* via predict API."""
    resp, err = imagen_predict(model_id, prompt, timeout=120)
    if err:
        return None, err
    try:
        b64 = resp["predictions"][0].get("bytesBase64Encoded") or resp["predictions"][0].get("b64")
        if not b64:
            return None, f"No image bytes in predictions: {str(resp)[:200]}"
        return base64.b64decode(b64), None
    except Exception as e:
        return None, f"Imagen parse: {e}: {str(resp)[:200]}"

def generate_thumbnail(post_id, prompt, out_path):
    """
    Priority:
    1. gemini-2.5-flash-image
    2. gemini-3.1-flash-image-preview
    3. imagen-4.0-fast-generate-001
    4. imagen-4.0-generate-001
    """
    attempts = [
        ("gemini-2.5-flash-image",           try_gemini_flash_image),
        ("gemini-3.1-flash-image-preview",   try_gemini_flash_image),
        ("imagen-4.0-fast-generate-001",     lambda p, m: try_imagen(p, m)),
        ("imagen-4.0-generate-001",          lambda p, m: try_imagen(p, m)),
    ]

    for model_id, fn in attempts:
        print(f"  [🎨 {model_id}] Generating...")
        img_bytes, err = fn(prompt, model_id)
        if img_bytes and len(img_bytes) > 1024:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"  [✅] Saved ({len(img_bytes)//1024}KB) → {os.path.basename(out_path)}")
            return True
        else:
            print(f"  [⚠️ ] {model_id} failed: {err}")

    # Log failure
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(os.path.join(LOGS_DIR, f"gen_thumb_{post_id}_err.log"), "w") as f:
        f.write(f"All models failed for post {post_id}\nPrompt: {prompt}\n")
    return False

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--limit",    type=int, default=10)
    parser.add_argument("--category", type=str)
    parser.add_argument("--sleep",    type=int, default=3)
    args = parser.parse_args()

    if not GEMINI_KEY:
        print("❌ No GEMINI_API_KEY found.")
        sys.exit(1)
    print(f"✅ GEMINI_API_KEY set. Using Gemini-only pipeline.")

    if not os.path.exists(GALLERY_DATA):
        print(f"❌ {GALLERY_DATA} not found.")
        sys.exit(1)

    os.makedirs(GALLERY_IMAGES_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        gallery_data = json.load(f)

    posts = gallery_data.get("posts", [])
    print(f"Loaded {len(posts)} posts")

    # Top 12 per category
    posts_by_cat = {}
    for p in posts:
        tags = p.get('tags', ['other'])
        cat  = tags[0] if tags else 'other'
        if cat not in CATEGORIES:
            cat = 'other'
        posts_by_cat.setdefault(cat, []).append(p)

    target_posts = []
    for cat in CATEGORIES:
        for p in posts_by_cat.get(cat, [])[:12]:
            p['primary_category'] = cat
            target_posts.append(p)

    print(f"Target (top 12×{len(CATEGORIES)} cats): {len(target_posts)} posts")

    if args.category:
        target_posts = [p for p in target_posts if p['primary_category'] == args.category]
        print(f"Filtered to '{args.category}': {len(target_posts)} posts")

    status = load_status()
    todo = []
    for p in target_posts:
        pid = str(p['id'])
        entry = status.get(pid, {})
        if entry.get("status") == "success":
            tp = entry.get("thumbnail_path","")
            fp = os.path.join(WORK_DIR, tp.lstrip("/"))
            if os.path.exists(fp) and os.path.getsize(fp) > 1024:
                continue
        todo.append(p)

    print(f"Remaining: {len(todo)} posts")
    if not todo:
        print("🎉 All done!")
        sys.exit(0)

    processed = 0
    for idx, p in enumerate(todo):
        if processed >= args.limit:
            print(f"\n⏸️  Batch limit {args.limit} reached.")
            break

        pid       = str(p['id'])
        caption   = p.get('caption','').replace('\n',' ')
        prompt    = p.get('prompt','')
        category  = p['primary_category']
        shortcode = p.get('shortcode', f"custom_{pid}")
        out_name  = f"threads_{shortcode}_0.png"
        out_path  = os.path.join(GALLERY_IMAGES_DIR, out_name)

        print(f"\n{'─'*60}")
        print(f"[{processed+1}/{min(args.limit, len(todo))}] Post {pid} | {category}")
        print(f"Caption: {caption[:70]}")
        print(f"Prompt:  {(prompt or '')[:80]}...")

        # Refinement check
        has_ph   = bool(re.search(r'\[.+?\]', prompt))
        is_kr    = any('\uac00' <= c <= '\ud7a3' for c in prompt)
        is_short = len(prompt.strip()) < 40
        needs_ref = has_ph or is_kr or is_short

        refined = prompt
        if needs_ref:
            print(f"  [Refine] Needed (ph={has_ph}, kr={is_kr}, short={is_short})")
            if not args.dry_run:
                refined = refine_prompt(prompt, caption, category)
                if not refined.strip():
                    refined = (
                        f"High-quality {category} style library thumbnail: {caption}. "
                        "Vivid colors, professional composition, sharp detail."
                    )
                print(f"  → {refined[:100]}...")
        else:
            print("  [Prompt] OK, no refinement.")

        if args.dry_run:
            print(f"  [DRY-RUN] → {out_name}")
            processed += 1
            continue

        ok = generate_thumbnail(pid, refined, out_path)

        url_path = f"/gallery-images/{out_name}"
        if ok:
            status[pid] = {
                "status": "success",
                "original_prompt": prompt,
                "refined_prompt": refined,
                "thumbnail_path": url_path,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            save_status(status)
            for gp in gallery_data.get("posts",[]):
                if gp.get("id") == p['id']:
                    gp['thumbnail'] = url_path
                    gp['prompt']    = refined
                    break
            with open(GALLERY_DATA,"w",encoding="utf-8") as f:
                json.dump(gallery_data, f, indent=2, ensure_ascii=False)
            processed += 1
        else:
            status[pid] = {
                "status": "failed",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            save_status(status)

        if idx < len(todo)-1 and processed < args.limit:
            print(f"  [⏱️ ] Sleeping {args.sleep}s...")
            time.sleep(args.sleep)

    print(f"\n{'='*60}")
    print(f"Done. Generated {processed} thumbnails this run.")

if __name__ == "__main__":
    main()
