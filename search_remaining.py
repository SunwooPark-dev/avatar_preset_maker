import json
import os

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
REPORT_FILE = os.path.join(WORK_DIR, "potential_issues_report.json")

def main():
    if not os.path.exists(REPORT_FILE):
        return

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        issues = json.load(f)

    targets = ["fenty", "shiseido", "kose", "sensual"]

    for item in issues:
        found = []
        for t in targets:
            if t in item.get("legal_violations", []) or t in item.get("gender_violations", []):
                found.append(t)
        
        if found:
            print(f"\nID: {item['id']} | Caption: {item['caption']}")
            print(f"Matched: {found}")
            print(f"Prompt: {item['prompt']}")

if __name__ == "__main__":
    main()
