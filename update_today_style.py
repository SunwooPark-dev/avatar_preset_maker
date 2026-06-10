# update_today_style.py - Daily Today's Style updater with Codex DALL-E 3 Thumbnail Generator
import os
import json
import shutil
import subprocess
import re
import datetime
import random

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
TODAY_STYLE_FILE = os.path.join(WORK_DIR, "today-style.json")
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")
ASSETS_DIR = os.path.join(WORK_DIR, "assets")
PREVIEW_THUMB = os.path.join(ASSETS_DIR, "today_style_preview.png")

# 10 predefined SNS Photo Trends/Memes (Cross-Ethnic & High Aesthetic)
TREND_COLLECTION = [
    {
        "theme": "Y2K Retro Camcorder",
        "description": "2000년대 Y2K 감성 저화질 디카 플래시 뷰티",
        "prompt": "Authentic Y2K early 2000s digital camera flash photography style portrait. High-contrast harsh direct flash, slightly soft focus, subtle lens glare, chromatic aberration, minor digital noise. Cool tone-balancing, pale blue and silver color grading. East Asian woman of mixed heritage wearing metallic puffer jacket and oversized futuristic sunglasses. Background: dark neon street alley at night. Expression: confident, playful look. Mood: nostalgic pop culture, Myspace era aesthetic.",
        "category": "photo"
    },
    {
        "theme": "90s Yearbook Photo",
        "description": "90년대 감성 레트로 미국 고등학교 졸업앨범 스타일",
        "prompt": "Nostalgic 1990s American high school yearbook portrait. Soft studio lighting, classic textured blue gradient backdrop. South Asian man wearing a vintage colorful knit sweater over a collared shirt. Clean parted hairstyle, gentle smile. Analog film warmth, subtle grain, classic portrait lens rendering. Mood: vintage retro school photo.",
        "category": "portrait"
    },
    {
        "theme": "Barbiecore Pink Fantasy",
        "description": "화려한 핫핑크 톤의 플라스틱 판타지 스타일",
        "prompt": "Vibrant Barbiecore pink aesthetic portrait. Intense monochrome hot pink palette. Black female model with sleek high ponytail, wearing glossy neon pink vinyl jacket and chunky pink retro sunglasses. Bright, high-key studio lighting with glossy pink plastic textures in the background. Bold makeup, confident smile. Fun, nostalgic toy aesthetic.",
        "category": "other"
    },
    {
        "theme": "Old Money Quiet Luxury",
        "description": "크림과 베이지 톤의 클래식 테니스 클럽 룩",
        "prompt": "Elegant old money aesthetic editorial portrait. Soft, warm natural sunlight. Latina woman with loose waves wearing a classic cream-colored cable-knit polo sweater, gold hoop earrings. Background: sun-drenched private tennis club with soft green foliage. Muted, sophisticated color grading, high-end film stock look. Quiet luxury, timeless style.",
        "category": "photo"
    },
    {
        "theme": "Cyberpunk Neon Hologram",
        "description": "네온 컬러와 자줏빛 글리치 홀로그램 사이버 테크웨어",
        "prompt": "Futuristic cyberpunk portrait featuring a Middle Eastern man with glowing neon blue cybernetic visor. Neon magenta and cyan rim lighting, atmospheric steam, holographic interface overlays. Wearing sleek black modular techwear jacket. Background: rainy dystopian Tokyo street, towering neon signs. High-tech, glitch art elements, dramatic shadows.",
        "category": "character"
    },
    {
        "theme": "Coquette Ribbon & Lace",
        "description": "로맨틱 빈티지 리본 앤 레이스 핑크 무드",
        "prompt": "Dreamy vintage coquette aesthetic portrait. South Asian woman with long braided hair decorated with multiple tiny pink satin ribbons. Wearing a delicate white lace corset and pearl necklace. Soft focus, warm pastel pink and cream color grading, ethereal lens flare. Background: soft-lit bedroom corner with vintage lace curtains and dried roses. Gentle, whimsical mood.",
        "category": "photo"
    },
    {
        "theme": "3D Clay Toy Model",
        "description": "귀여운 점토 애니메이션 스타일의 3D 아바타",
        "prompt": "Adorable 3D claymation toy character portrait of an East Asian boy. Smooth matte clay textures, stylized big expressive eyes, cute clay hair. Wearing a tiny colorful puffer jacket. Colorful geometric blocks in the background with soft studio lighting and clean ambient occlusion. Whimsical clay art style, high-quality 3D render.",
        "category": "illustration"
    },
    {
        "theme": "Retro Classic Anime Screen",
        "description": "80-90년대 클래식 셀 채색 애니메이션 뷰",
        "prompt": "Retro 1980s aesthetic hand-drawn classic anime screenshot portrait. South Asian girl with large expressive hand-drawn anime eyes, slightly blowing hair, vintage cell-shaded illustration style. Soft pastel sunset colors, retro CRT screen scanlines, subtle chromatic aberration. Background: a scenic train window showing rural fields under a soft orange sky.",
        "category": "illustration"
    },
    {
        "theme": "Pixar 3D Animation Style",
        "description": "입체적이고 생생한 디즈니 픽사 애니메이션 스타일",
        "prompt": "Stunning Pixar and Disney 3D animation style portrait. Black male character with highly expressive amber eyes, stylized features, friendly warm smile. Realistic hair shader, fine clothing fabric details. Background: cozy warm-lit library with soft bokeh. Perfect rim lighting, high-end global illumination, cinematic rendering.",
        "category": "character"
    },
    {
        "theme": "Zombie Apocalypse Survivor",
        "description": "종말을 해치고 살아남은 거칠고 영화적인 생존자 프로필",
        "prompt": "Grungy post-apocalyptic survivor portrait. Latino man with dirt and ash smudges on his face, wearing a weathered leather jacket and tactical gear. Dramatic high-contrast cinematic lighting with volumetric dust particles. Background: ruined concrete urban wasteland under dark overcast skies. Gritty textures, movie poster aesthetic, intense focus.",
        "category": "portrait"
    }
]

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

def get_clean_env() -> dict:
    env = os.environ.copy()
    key = env.get("OPENAI_API_KEY", "")
    if key.startswith("\ufeff"):
        env["OPENAI_API_KEY"] = key.lstrip("\ufeff").strip()
    return env

_CLEAN_ENV = get_clean_env()

def select_today_style():
    # Use the day of the year to cycle through the 10 trends deterministically
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    index = (day_of_year - 1) % len(TREND_COLLECTION)
    return TREND_COLLECTION[index]

def generate_preview_thumbnail(prompt):
    """Generate the preview image for Today's Style using Codex CLI."""
    print("Generating Today's Style preview thumbnail via Codex...")
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    # Instruct Codex to use DALL-E 3 with Gemini fallback
    model_instruction = (
        "Model Preference: Generate the image using the ChatGPT Image 2.0 (DALL-E 3) model by default. "
        "If DALL-E 3 fails, fall back to Google Nano Banana (Gemini Image Generation) as the secondary option."
    )
    codex_prompt = (
        f"Use the generate_image tool to generate a stunning style preview image for Today's Style: {prompt}. "
        f"{model_instruction} "
        f"Save the final generated image file to assets/today_style_preview.png in the current directory."
    )
    
    cmd = [
        CODEX_CLI,
        "exec",
        codex_prompt,
        "-c", "model_reasoning_effort=low",
        "--dangerously-bypass-approvals-and-sandbox",
        "--ephemeral"
    ]
    
    try:
        res = subprocess.run(
            cmd,
            cwd=WORK_DIR,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=240,
            env=_CLEAN_ENV
        )
        print(res.stdout)
        print(res.stderr)
        
        # Look if the file is generated in ~/.codex/generated_images or output path
        # Simple fallback: if not saved in target path, check ~/.codex/generated_images
        if os.path.exists(PREVIEW_THUMB) and os.path.getsize(PREVIEW_THUMB) > 1024:
            print("Successfully generated Today's Style preview thumbnail!")
            return True
        else:
            # Inspect ~/.codex/generated_images
            gen_dir = os.path.join(os.path.expanduser("~"), ".codex", "generated_images")
            if os.path.isdir(gen_dir):
                # Search all sessions
                png_files = []
                for root, dirs, files in os.walk(gen_dir):
                    for f in files:
                        if f.endswith('.png'):
                            png_files.append(os.path.join(root, f))
                if png_files:
                    png_files.sort(key=os.path.getmtime, reverse=True)
                    newest = png_files[0]
                    if os.path.getsize(newest) > 1024:
                        shutil.copy(newest, PREVIEW_THUMB)
                        print(f"Recovered generated image from {newest} to {PREVIEW_THUMB}")
                        return True
            print("Warning: Thumbnail was not generated or found.")
            return False
    except Exception as e:
        print(f"Error calling Codex CLI: {e}")
        return False

def update_json_files(style_data):
    # 1. Update today-style.json
    with open(TODAY_STYLE_FILE, "w", encoding="utf-8") as f:
        json.dump(style_data, f, indent=2, ensure_ascii=False)
    print("Updated today-style.json")

    # 2. Update gallery-data.json (Insert as first post so it filters under "오늘의 밈" tab)
    if os.path.exists(GALLERY_DATA):
        try:
            with open(GALLERY_DATA, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            posts = data.get("posts", [])
            # Filter out previous "today" items
            posts = [p for p in posts if p.get("id") != 90999 and "today" not in p.get("tags", [])]
            
            # Create today post item
            today_post = {
                "id": 90999,
                "tags": ["today", style_data.get("category", "photo"), "trend"],
                "shortcode": "today_style",
                "caption": f"오늘의 Style: {style_data['theme']}",
                "prompt": style_data["prompt"],
                "primary_category": "today",
                "thumbnail": "/assets/today_style_preview.png"
            }
            
            # Insert at the beginning
            posts.insert(0, today_post)
            
            data["posts"] = posts
            data["totalPosts"] = len(posts)
            
            # Save updated gallery-data.json
            with open(GALLERY_DATA, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("Updated gallery-data.json with Today's Style post.")
        except Exception as e:
            print(f"Error updating gallery-data.json: {e}")

if __name__ == "__main__":
    print("Starting Today's Style rotation and update process...")
    style_data = select_today_style()
    print(f"Selected Style: {style_data['theme']}")
    print(f"Prompt: {style_data['prompt']}")
    
    # 1. Update JSON files first so API serves it instantly
    update_json_files(style_data)
    
    # 2. Call Codex to generate preview thumbnail
    success = generate_preview_thumbnail(style_data["prompt"])
    if not success:
        # Fallback to copy default cat image if generation failed
        print("Using default fallback thumbnail image...")
        fallback_src = os.path.join(WORK_DIR, "cat.png")
        if os.path.exists(fallback_src):
            shutil.copy(fallback_src, PREVIEW_THUMB)
            print("Copied default fallback to today_style_preview.png")
    
    print("Today's Style rotation complete!")
