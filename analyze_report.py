import json
import os
from collections import Counter

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
REPORT_FILE = os.path.join(WORK_DIR, "potential_issues_report.json")

def main():
    if not os.path.exists(REPORT_FILE):
        print("Error: potential_issues_report.json not found")
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        issues = json.load(f)

    print(f"Total issues: {len(issues)}")

    legal_words = []
    gender_words = []

    for item in issues:
        legal_words.extend(item.get("legal_violations", []))
        gender_words.extend(item.get("gender_violations", []))

    legal_counter = Counter(legal_words)
    gender_counter = Counter(gender_words)

    print("\n=== Legal Keyword Frequencies ===")
    for word, count in legal_counter.most_common():
        print(f"  {word}: {count}")

    print("\n=== Gender Keyword Frequencies ===")
    for word, count in gender_counter.most_common():
        print(f"  {word}: {count}")

    # Print a few samples
    print("\n=== Sample Issues ===")
    for i, item in enumerate(issues[:10]):
        print(f"\n[{i+1}] ID: {item['id']} | Caption: {item['caption']}")
        print(f"    Legal Violations: {item['legal_violations']}")
        print(f"    Gender Violations: {item['gender_violations']}")
        print(f"    Prompt sample: {item['prompt'][:120]}...")

if __name__ == "__main__":
    main()
