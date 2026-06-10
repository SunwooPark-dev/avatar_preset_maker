# generate_thumbnails.py - Automated style library thumbnail generator
import os
import json
import shutil
import subprocess
import time
import re
import sys
import argparse

def find_codex_cli():
    import glob
    base_dir = r"C:\Users\sunwo\AppData\Local\OpenAI\Codex\bin"
    if not os.path.exists(base_dir):
        return "codex"
    exe_files = glob.glob(os.path.join(base_dir, "**", "codex.exe"), recursive=True)
    if exe_files:
        exe_files.sort(key=os.path.getmtime, reverse=True)
        return exe_files[0]
    return "codex"

CODEX_CLI = find_codex_cli()
WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
SOURCE_PNG = os.path.join(WORK_DIR, "source.png")
STATUS_FILE = os.path.join(WORK_DIR, "thumbnail_generation_status.json")
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")
GALLERY_IMAGES_DIR = os.path.join(WORK_DIR, "gallery-images")

# Categories mapping
CATEGORIES = ['portrait', 'illustration', 'product', 'food', 'character', 'plush', 'poster', 'sticker', 'photo', 'infographic', 'design', 'other']

# Clean environment that strips BOM from OPENAI_API_KEY
def get_clean_env() -> dict:
    env = os.environ.copy()
    key = env.get("OPENAI_API_KEY", "")
    if key.startswith("\ufeff"):
        env["OPENAI_API_KEY"] = key.lstrip("\ufeff").strip()
    return env

_CLEAN_ENV = get_clean_env()

def load_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_status(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)

def refine_prompt_via_codex(prompt, caption, category):
    """Call Codex to refine/translate the prompt into a high-quality DALL-E/Imagen prompt."""
    codex_instruction = (
        f"Optimize and rewrite this image generation prompt to be detailed, clear, and in English. "
        f"Fill in any bracketed placeholders like [CHARACTER], [DESTINATION], [배경색] or [인물] with concrete, visually rich examples suitable for a style library thumbnail. "
        f"Translate to English if it is in Korean. Output ONLY the refined English prompt. No explanation, no intro.\n\n"
        f"Category: {category}\n"
        f"Caption: {caption}\n"
        f"Prompt: {prompt}"
    )
    
    cmd = [
        CODEX_CLI,
        "exec",
        codex_instruction,
        "-c", "model_reasoning_effort=low",
        "--dangerously-bypass-approvals-and-sandbox",
        "--ephemeral"
    ]
    
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=_CLEAN_ENV
        )
        if res.returncode == 0:
            refined = res.stdout.strip()
            # Clean up potential wrapped quotes or markdown backticks
            refined = re.sub(r'^["\'`]+|["\'`]+$', '', refined).strip()
            if refined:
                return refined
        return prompt
    except Exception as e:
        print(f"Warning: Prompt refinement failed: {e}")
        return prompt

def generate_image_via_codex(post_id, refined_prompt, is_portrait, shortcode):
    """Generate image via Codex CLI exec, copying output to gallery-images."""
    out_name = f"threads_{shortcode}_0.png"
    out_path = os.path.join(GALLERY_IMAGES_DIR, out_name)
    
    # If portrait-like, copy source.png and attach it
    src_name = None
    if is_portrait:
        src_name = f"source_thumb_{post_id}.png"
        src_path = os.path.join(WORK_DIR, src_name)
        if os.path.exists(SOURCE_PNG):
            shutil.copy(SOURCE_PNG, src_path)
        else:
            print(f"Error: source.png not found at {SOURCE_PNG}")
            return None
            
    # Build prompt to Codex with explicit model preference: ChatGPT Image 2.0 (DALL-E 3) default, Google Nano Banana (Gemini) fallback.
    model_instruction = (
        "Model Preference: Generate the image using the ChatGPT Image 2.0 (DALL-E 3) model by default. "
        "If DALL-E 3 is blocked (e.g. by safety/content filters) or fails, "
        "fall back (rollback) to the Google Nano Banana (Gemini Image Generation / Google Image 2.0) model as the sub/secondary option."
    )

    if is_portrait:
        codex_prompt = (
            f"I have attached the source image via -i flag. "
            f"Preserve this person's face structure and features. "
            f"Use the generate_image tool with the attached image as the base to apply this style: {refined_prompt}. "
            f"{model_instruction} "
            f"Save the final generated image file to gallery-images/{out_name} in the current directory."
        )
        cmd = [
            CODEX_CLI,
            "exec",
            codex_prompt,
            "-i", src_name,
            "-c", "model_reasoning_effort=low",
            "--dangerously-bypass-approvals-and-sandbox",
            "--ephemeral"
        ]
    else:
        codex_prompt = (
            f"Use the generate_image tool to generate a high-quality style preview image representing: {refined_prompt}. "
            f"{model_instruction} "
            f"Save the final generated image file to gallery-images/{out_name} in the current directory."
        )
        cmd = [
            CODEX_CLI,
            "exec",
            codex_prompt,
            "-c", "model_reasoning_effort=low",
            "--dangerously-bypass-approvals-and-sandbox",
            "--ephemeral"
        ]
        
    print(f"Generating thumbnail for Post {post_id} (portrait={is_portrait})...")
    
    # Create logs directory
    logs_dir = os.path.join(WORK_DIR, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_err = os.path.join(logs_dir, f"gen_thumb_{post_id}_err.log")
    
    proc = None
    success = False
    session_id = None
    session_pattern = re.compile(r"session id:\s*([a-f0-9\-]+)", re.IGNORECASE)
    
    try:
        with open(log_err, "w", encoding="utf-8") as ferr:
            proc = subprocess.Popen(
                cmd,
                cwd=WORK_DIR,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=_CLEAN_ENV
            )
            
            # Read stdout line by line to capture session ID
            for line in proc.stdout:
                ferr.write(line)
                ferr.flush()
                # Print live output
                print(f"  [Codex]: {line.strip()}")
                
                # Check for session ID
                if not session_id:
                    m = session_pattern.search(line)
                    if m:
                        session_id = m.group(1)
                        print(f"  [Codex Session]: {session_id}")
                        
        proc.wait()
        
        # Check if file exists in target path
        if os.path.exists(out_path) and os.path.getsize(out_path) > 1024:
            success = True
        elif session_id:
            # Check ~/.codex/generated_images/{session_id}/
            gen_dir = os.path.join(os.path.expanduser("~"), ".codex", "generated_images", session_id)
            if os.path.isdir(gen_dir):
                png_files = [os.path.join(gen_dir, f) for f in os.listdir(gen_dir) if f.endswith('.png')]
                if png_files:
                    png_files.sort(key=os.path.getmtime, reverse=True)
                    target_img = png_files[0]
                    if os.path.getsize(target_img) > 1024:
                        shutil.copy(target_img, out_path)
                        success = True
                        print(f"  [Backup Copy]: Copied image from generated_images folder to {out_path}")
                        
    except Exception as e:
        print(f"Error during Codex generation for Post {post_id}: {e}")
    finally:
        # Cleanup temp source file
        if is_portrait and src_name:
            try:
                src_path = os.path.join(WORK_DIR, src_name)
                if os.path.exists(src_path):
                    os.remove(src_path)
            except Exception:
                pass
                
    if success:
        print(f"✅ SUCCESS: Generated {out_name} for Post {post_id}")
        return f"/gallery-images/{out_name}"
    else:
        print(f"❌ FAILED: Failed to generate image for Post {post_id}. Check log: {log_err}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate style library thumbnails via Codex")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be done without calling Codex")
    parser.add_argument("--limit", type=int, default=5, help="Maximum number of thumbnails to generate in this run")
    parser.add_argument("--category", type=str, help="Only process this category")
    parser.add_argument("--sleep", type=int, default=60, help="Sleep seconds between generations")
    args = parser.parse_args()
    
    if not os.path.exists(GALLERY_DATA):
        print(f"Error: {GALLERY_DATA} not found.")
        sys.exit(1)
        
    os.makedirs(GALLERY_IMAGES_DIR, exist_ok=True)
    
    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        gallery_data = json.load(f)
        
    posts = gallery_data.get("posts", [])
    print(f"Loaded {len(posts)} posts from gallery-data.json")
    
    # Group posts by tag
    posts_by_category = {}
    for p in posts:
        tags = p.get('tags', ['other'])
        primary_tag = tags[0] if tags else 'other'
        if primary_tag not in CATEGORIES:
            primary_tag = 'other'
        posts_by_category.setdefault(primary_tag, []).append(p)
        
    # Get top 12 for each category
    target_posts = []
    category_counts = {}
    for cat in CATEGORIES:
        cat_posts = posts_by_category.get(cat, [])
        top_12 = cat_posts[:12]
        category_counts[cat] = len(top_12)
        for p in top_12:
            p['primary_category'] = cat
            target_posts.append(p)
            
    print("\nTarget Posts Counts (Top 12 per Category):")
    for cat, count in category_counts.items():
        print(f"  {cat}: {count} posts")
    print(f"Total target posts: {len(target_posts)}")
    
    if args.category:
        target_posts = [p for p in target_posts if p['primary_category'] == args.category]
        print(f"Filtered to category '{args.category}': {len(target_posts)} posts")
        
    # Load status registry
    status_registry = load_status()
    
    # Filter out already successfully processed posts
    todo_posts = []
    for p in target_posts:
        pid = str(p['id'])
        if pid in status_registry and status_registry[pid].get("status") == "success":
            # If thumbnail file exists, skip
            thumb_path = status_registry[pid].get("thumbnail_path")
            full_thumb_path = os.path.join(WORK_DIR, thumb_path.lstrip("/"))
            if os.path.exists(full_thumb_path):
                continue
        todo_posts.append(p)
        
    print(f"Remaining posts to process: {len(todo_posts)}")
    
    if not todo_posts:
        print("All target thumbnails already generated!")
        sys.exit(0)
        
    # Process batch
    processed_count = 0
    for p in todo_posts:
        if processed_count >= args.limit:
            print(f"\nReached batch limit of {args.limit} posts. Stopping.")
            break
            
        pid = str(p['id'])
        caption = p.get('caption', '')
        prompt = p.get('prompt', '')
        category = p['primary_category']
        shortcode = p.get('shortcode', f"custom_{pid}")
        is_portrait = category in ['portrait', 'character', 'photo']
        
        print(f"\n--- Processing Post {pid} (Category: {category}) ---")
        print(f"Caption: {caption.replace(chr(10), ' ')}")
        print(f"Original Prompt: {prompt[:100]}...")
        
        # Decide if prompt needs refinement
        has_placeholders = '[' in prompt or ']' in prompt or 'placeholder' in prompt.lower()
        is_korean = any('\uac00' <= char <= '\ud7a3' for char in prompt)
        is_short = len(prompt) < 40
        needs_refinement = has_placeholders or is_korean or is_short
        
        refined_prompt = prompt
        if needs_refinement:
            print(f"Prompt needs refinement (placeholders={has_placeholders}, korean={is_korean}, short={is_short}).")
            if args.dry_run:
                refined_prompt = f"[DRY-RUN REFINED PROMPT for: {prompt[:30]}]"
            else:
                refined_prompt = refine_prompt_via_codex(prompt, caption, category)
                print(f"Refined Prompt: {refined_prompt}")
        else:
            print("Prompt is clean. Skipping refinement.")
            
        if args.dry_run:
            print(f"[DRY-RUN] Would generate image for Post {pid} with refined prompt: {refined_prompt}")
            processed_count += 1
            continue
            
        # Update prompt in memory
        p['prompt'] = refined_prompt
        
        # Generate thumbnail
        thumb_url = generate_image_via_codex(p['id'], refined_prompt, is_portrait, shortcode)
        
        if thumb_url:
            # Update post thumbnail in memory
            p['thumbnail'] = thumb_url
            
            # Save status
            status_registry[pid] = {
                "status": "success",
                "original_prompt": prompt,
                "refined_prompt": refined_prompt,
                "thumbnail_path": thumb_url,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            save_status(status_registry)
            
            # Save updated gallery-data.json
            # Find the original post in gallery_data and update it
            for gp in gallery_data.get("posts", []):
                if gp.get("id") == p['id']:
                    gp['thumbnail'] = thumb_url
                    gp['prompt'] = refined_prompt
                    break
            with open(GALLERY_DATA, "w", encoding="utf-8") as f:
                json.dump(gallery_data, f, indent=2, ensure_ascii=False)
                
            processed_count += 1
            
            # Sleep between generations to protect Codex OAuth quota
            if processed_count < args.limit:
                print(f"Sleeping {args.sleep} seconds to preserve quota...")
                time.sleep(args.sleep)
        else:
            status_registry[pid] = {
                "status": "failed",
                "error": "Failed to generate thumbnail via Codex",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            save_status(status_registry)
            # Sleep anyway to protect quota
            time.sleep(10)

    print(f"\nBatch finished. Processed {processed_count} posts.")

if __name__ == '__main__':
    main()
