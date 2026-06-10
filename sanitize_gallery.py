import json
import os
import re

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")
STATUS_FILE = os.path.join(WORK_DIR, "thumbnail_generation_status.json")

CATEGORIES = [
    'portrait','illustration','product','food','character',
    'plush','poster','sticker','photo','infographic','design','other'
]

# Replacement mapping (key -> (replacement, is_regex))
# Using word boundaries (\b) or raw string replacement.
# Case-insensitive replacements.
REPLACEMENTS = {
    # 1. Legal / Brands / IPs
    r"\bnike\b": "premium athletic sportswear",
    r"\badidas\b": "premium sportswear",
    r"\brolex\b": "luxury Swiss chronograph watch",
    r"\bdior\b": "luxury designer fashion",
    r"\bchanel\b": "luxury fashion house",
    r"\bgucci\b": "high-end luxury brand",
    r"\bprada\b": "luxury designer fashion",
    r"\btom ford\b": "luxury designer brand",
    r"\bvalentino\b": "luxury designer brand",
    r"\bbyredo\b": "luxury fragrance house",
    r"\ble labo\b": "premium fragrance brand",
    r"\bforest essentials\b": "premium Ayurvedic luxury brand",
    r"\bjellycat\b": "premium soft designer plush",
    r"\bmaileg\b": "heritage soft plush design",
    r"\bnici\b": "premium soft plush brand",
    r"\bwild republic\b": "nature-themed plush toy brand",
    r"\bkeel toys\b": "premium soft plush brand",
    r"\bgq\b": "high-fashion men's magazine",
    r"\bvogue\b": "high-fashion editorial magazine",
    r"\bforbes\b": "business leadership magazine",
    r"\bessence\b": "premium lifestyle publication",
    r"\bdisney\b": "iconic family animation studio",
    r"\bpixar\b": "iconic 3D animation studio",
    r"\bmarvel\b": "superhero adventure franchise",
    r"\bstar wars\b": "epic sci-fi space opera franchise",
    r"\bpokemon\b": "pocket monster adventure game style",
    r"\bnintendo\b": "classic video game console aesthetic",
    r"\blego\b": "interlocking plastic toy bricks",
    r"\bbarbie\b": "fashion doll aesthetic",
    r"\bghibli\b": "nostalgic hand-painted anime style",
    r"\bkakao\b": "popular character mascot style",
    r"\bline friends\b": "minimalist cute character mascot style",
    r"\bbolshoi\b": "world-class theatrical stage",
    r"\bmickey\b": "famous cartoon mouse character",
    r"\belsa\b": "magical ice princess character",
    r"\bfrozen\b": "magical ice fantasy story",
    r"\bwitcher\b": "dark fantasy monster hunter world",
    r"\bfate/stay night\b": "action fantasy anime visual style",
    r"\bghost of tsushima\b": "historical cinematic samurai game aesthetic",
    r"\bnational geographic\b": "renowned documentary publication",
    r"\bdazed & confused\b": "avant-garde fashion magazine",
    r"\bfenty\b": "premium beauty cosmetics",
    r"\bshiseido\b": "premium beauty cosmetics",
    r"\bkose\b": "premium beauty cosmetics",
    
    # Celebrities / Public figures
    r"\biu\b": "popular celebrity",
    r"\bbts\b": "famous pop band",
    r"\bjennie\b": "famous pop artist",
    r"\bjisoo\b": "popular pop artist",
    r"\blisa\b": "popular pop artist",
    r"\brose\b": "romantic", # Keep rose as is if flower, but check if we should replace. Actually 'rose' is mostly flower. We should only replace 'rose' when it refers to the blackpink member, which is rare. Let's skip replacing 'rose' universally to avoid ruining flower prompts.
    r"\bblackpink\b": "famous pop group",
    r"\bnewjeans\b": "popular pop band",
    r"\bive\b": "popular pop group",
    r"\baespa\b": "famous pop group",
    r"\btwice\b": "popular pop group",
    r"\bred velvet\b": "rich crimson", # Usually cake or velvet dress
    r"\bsuzy\b": "popular celebrity",
    r"\bwonyoung\b": "famous pop artist",
    r"\bkarina\b": "famous pop artist",
    r"\bdiego rivera\b": "classic muralist",
    r"\boscar niemeyer\b": "classic modern architectural curves",
    r"\bhélio oiticica\b": "modern geometric abstract art style",
    r"\blygia clark\b": "interactive modernist abstract art style",
    r"\banne rice\b": "classic gothic romance novelist",

    # 2. Gender / Sexualization
    r"\blolita\b": "classic Victorian doll-like",
    r"\bsexy\b": "charismatic",
    r"\bseductive\b": "confident",
    r"\bprovocative\b": "striking",
    r"\bsensual\b": "charismatic",
    r"\bhot\b": "vibrant",
    r"\bcleavage\b": "tasteful neckline",
    r"\bbusty\b": "well-tailored",
    r"\brevealing\b": "stylish",
    r"\bexposing\b": "modern",
    r"\bbikini\b": "athletic swimwear",
    r"\bswimsuit\b": "athletic swimwear",
    r"\bnude\b": "natural skin tone",
    r"\bnaked\b": "natural skin tone",
    r"\bshirtless\b": "relaxed casual outfit"
}

# Special manual cleanups for rose and red velvet if they are indeed celebrities in the prompt
def clean_special_cases(text):
    # If 'rose' is near 'blackpink', change it
    text = re.sub(r"\bRosé\b", "popular pop artist", text, flags=re.IGNORECASE)
    # If red velvet refers to K-pop group
    text = re.sub(r"\bRed Velvet members\b", "famous pop artists", text, flags=re.IGNORECASE)
    text = re.sub(r"\bRed Velvet K-pop\b", "famous K-pop group", text, flags=re.IGNORECASE)
    return text

def sanitize_text(text):
    if not text:
        return text
    
    text = clean_special_cases(text)
    
    for pattern, replacement in REPLACEMENTS.items():
        if pattern == r"\brose\b" or pattern == r"\bred velvet\b":
            continue
        new_text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        if new_text != text:
            print(f"    [MATCHED] {pattern} -> {replacement}")
            text = new_text
        
    return text

def main():
    if not os.path.exists(GALLERY_DATA):
        print("Error: gallery-data.json not found")
        return

    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        gallery_data = json.load(f)

    posts = gallery_data.get("posts", [])
    print(f"Loaded {len(posts)} posts for sanitization")

    # Determine which posts are in the current top 12 per category
    posts_by_cat = {}
    for p in posts:
        tags = p.get('tags', ['other'])
        cat  = tags[0] if tags else 'other'
        if cat not in CATEGORIES:
            cat = 'other'
        posts_by_cat.setdefault(cat, []).append(p)

    target_ids = set()
    for cat in CATEGORIES:
        for p in posts_by_cat.get(cat, [])[:12]:
            target_ids.add(p['id'])

    modified_count = 0
    modified_targets = []

    for p in posts:
        pid = p.get("id")
        orig_prompt = p.get("prompt", "")
        orig_caption = p.get("caption", "")

        sanitized_prompt = sanitize_text(orig_prompt)
        sanitized_caption = sanitize_text(orig_caption)

        is_modified = (orig_prompt != sanitized_prompt) or (orig_caption != sanitized_caption)

        if is_modified:
            p["prompt"] = sanitized_prompt
            p["caption"] = sanitized_caption
            modified_count += 1
            if pid in target_ids:
                modified_targets.append(pid)

    print(f"Sanitized {modified_count} posts total.")
    print(f"Found {len(modified_targets)} modified posts within the top 12 categories.")

    # Save sanitized gallery-data.json
    with open(GALLERY_DATA, "w", encoding="utf-8") as f:
        json.dump(gallery_data, f, indent=2, ensure_ascii=False)
    print("gallery-data.json updated successfully.")

    # Clear status for modified targets to force thumbnail regeneration
    if modified_targets:
        if os.path.exists(STATUS_FILE):
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                status = json.load(f)
            
            removed_count = 0
            for pid in modified_targets:
                spid = str(pid)
                if spid in status:
                    status.pop(spid)
                    removed_count += 1
            
            with open(STATUS_FILE, "w", encoding="utf-8") as f:
                json.dump(status, f, indent=2, ensure_ascii=False)
            
            print(f"Cleared status for {removed_count} target posts in {STATUS_FILE} to trigger regeneration.")
        else:
            print("No status file found to clear.")

if __name__ == "__main__":
    main()
