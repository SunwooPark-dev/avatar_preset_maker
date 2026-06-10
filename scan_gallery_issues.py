import json
import os
import re

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")

# 1. Legal risk keywords (brands, celebrities, copyrighted IPs)
LEGAL_KEYWORDS = [
    # Brands & Fashion
    "nike", "adidas", "rolex", "dior", "chanel", "gucci", "prada", "fenty", "shiseido", "kose",
    "tom ford", "valentino", "byredo", "le labo", "forest essentials", "jellycat", "maileg", "nici",
    "wild republic", "keel toys", "gq", "vogue", "forbes", "essence", "starbucks", "apple", "samsung",
    # Entertainment & IPs
    "disney", "pixar", "marvel", "star wars", "pokemon", "nintendo", "lego", "barbie", "ghibli",
    "kakao", "line friends", "line", "bolshoi", "mickey", "elsa", "frozen", "witcher", "fate/stay night",
    "ghost of tsushima", "anime", "manga", "k-pop", "kpop", "dazed & confused", "national geographic",
    # Celebrities / Public figures
    "iu", "bts", "jennie", "jisoo", "lisa", "rose", "blackpink", "newjeans", "ive", "aespa",
    "twice", "red velvet", "suzy", "wonyoung", "karina", "chawan", "diego rivera", "oscar niemeyer",
    "hélio oiticica", "lygia clark", "anne rice"
]

# 2. Gender & Sexualization risk keywords
GENDER_KEYWORDS = [
    "sexy", "hot", "sensual", "erotic", "seductive", "slinky", "revealing", "cleavage", "busty",
    "lolita", "provocative", "exposing", "naked", "bare chest", "shirtless", "nude", "underwear",
    "lingerie", "bikini", "swimsuit", "skimp", "fetish", "erogenous", "lascivious", "lewd"
]

def scan_gallery():
    if not os.path.exists(GALLERY_DATA):
        print("Error: gallery-data.json not found")
        return

    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    print(f"Total posts to scan: {len(posts)}")

    issues = []

    for p in posts:
        pid = p.get("id")
        prompt = (p.get("prompt") or "").lower()
        caption = (p.get("caption") or "").lower()
        tags = [t.lower() for t in p.get("tags", [])]

        found_legal = []
        found_gender = []

        # Scan legal keywords
        for kw in LEGAL_KEYWORDS:
            # Match word boundary to avoid false positives (like 'line' matching in 'skyline')
            pattern = rf"\b{re.escape(kw)}\b"
            if re.search(pattern, prompt) or re.search(pattern, caption):
                found_legal.append(kw)

        # Scan gender keywords
        for kw in GENDER_KEYWORDS:
            pattern = rf"\b{re.escape(kw)}\b"
            if re.search(pattern, prompt) or re.search(pattern, caption):
                found_gender.append(kw)

        if found_legal or found_gender:
            issues.append({
                "id": pid,
                "caption": p.get("caption"),
                "prompt": p.get("prompt"),
                "legal_violations": found_legal,
                "gender_violations": found_gender
            })

    print(f"\nScan complete. Found {len(issues)} posts with potential issues.")
    
    # Save results to a report file
    report_path = os.path.join(WORK_DIR, "potential_issues_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2, ensure_ascii=False)
    
    print(f"Report saved to: {report_path}")

    # Summary by type
    legal_count = sum(1 for i in issues if i["legal_violations"])
    gender_count = sum(1 for i in issues if i["gender_violations"])
    both_count = sum(1 for i in issues if i["legal_violations"] and i["gender_violations"])

    print(f"  - Legal issues only: {legal_count - both_count}")
    print(f"  - Gender issues only: {gender_count - both_count}")
    print(f"  - Both issues: {both_count}")

if __name__ == "__main__":
    scan_gallery()
