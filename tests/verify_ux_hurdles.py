# tests/verify_ux_hurdles.py
import time
import os
from playwright.sync_api import sync_playwright

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)
CAT_PNG = os.path.join(PROJECT_DIR, "cat.png")
SCREENSHOTS_DIR = os.path.join(TEST_DIR, "screenshots")

def run_verification():
    print("=== STARTING UX HURDLES MINIMIZATION VERIFICATION ===")
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()
        
        # Log browser console
        page.on("console", lambda msg: print(f"Browser Console: [{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"Browser Page Error: {err}"))
        
        try:
            print("1. Navigating to local site...")
            page.goto("http://127.0.0.1:8080/?mock=true")
            page.wait_for_load_state("networkidle")
            
            print("2. Verifying Initial State (Privacy Shield & Sliders)...")
            initial_screenshot_path = os.path.join(SCREENSHOTS_DIR, "ux_initial_state.png")
            page.screenshot(path=initial_screenshot_path)
            print(f"  - Initial state screenshot saved: {initial_screenshot_path}")
            
            banner = page.locator(".privacy-shield-banner")
            if banner.is_visible():
                print("  - [PASS] Privacy Shield Banner is visible!")
            else:
                print("  - [FAIL] Privacy Shield Banner is NOT visible!")
                
            # Verify tooltips (info badges) are present
            info_badges = page.locator(".info-badge")
            badge_count = info_badges.count()
            print(f"  - Found {badge_count} info badge elements.")
            if badge_count == 3:
                print("  - [PASS] Exactly 3 info badges found next to sliders.")
            else:
                print(f"  - [FAIL] Expected 3 info badges, found {badge_count}.")
                
            # Verify multi-language selector changes texts on selection
            print("  - Testing language selector (switching to English)...")
            page.select_option("#lang-select", "en")
            weight_label = page.locator("[data-i18n='slider_weight_title']").text_content().strip()
            print(f"  - Prompt Weight Label in EN: '{weight_label}'")
            if weight_label == "Prompt Weight":
                print("  - [PASS] Language switcher to EN works!")
            else:
                print(f"  - [FAIL] Switcher to EN failed, got '{weight_label}'")

            print("  - Testing language selector (switching to Korean)...")
            page.select_option("#lang-select", "ko")
            weight_label_ko = page.locator("[data-i18n='slider_weight_title']").text_content().strip()
            print(f"  - Prompt Weight Label in KO: '{weight_label_ko}'")
            if weight_label_ko == "프롬프트 반영 강도":
                print("  - [PASS] Language switcher to KO works!")
            else:
                print(f"  - [FAIL] Switcher to KO failed, got '{weight_label_ko}'")
            
            # 3. Upload image
            print("3. Uploading cat.png...")
            file_input = page.locator("input#file-input")
            file_input.set_input_files(CAT_PNG)
            
            # Wait until the Render Style button is enabled
            page.wait_for_selector("#generate-btn:not([disabled])", timeout=10000)
            print("  - [PASS] Render Style button is enabled after upload.")
            
            # 4. Click Render Style button and test scroll/rolling status
            print("4. Triggering Render Style...")
            page.click("#generate-btn")
            
            # Wait a moment for scroll and loading screen
            time.sleep(1)
            
            processing_screenshot_path = os.path.join(SCREENSHOTS_DIR, "ux_processing_state_1.png")
            page.screenshot(path=processing_screenshot_path)
            
            status_el = page.locator("#processing-status")
            status_text_1 = status_el.text_content().strip()
            print(f"  - Processing status message 1: '{status_text_1}'")
            
            time.sleep(2.5)
            status_text_2 = status_el.text_content().strip()
            print(f"  - Processing status message 2: '{status_text_2}'")
            
            processing_screenshot_path_2 = os.path.join(SCREENSHOTS_DIR, "ux_processing_state_2.png")
            page.screenshot(path=processing_screenshot_path_2)
            
            if status_text_1 != status_text_2:
                print("  - [PASS] Status rolling works!")
            else:
                print("  - [WARNING] Status rolling did not change text.")
                
            # 5. Wait for mock/real rendering completion
            print("5. Waiting for render completion...")
            page.wait_for_selector("#state-ready:not(.hidden)", timeout=120000)
            print("  - [PASS] Processing completed, Ready state shown.")
            
            ready_screenshot_path = os.path.join(SCREENSHOTS_DIR, "ux_ready_state.png")
            page.screenshot(path=ready_screenshot_path)
            
        except Exception as e:
            error_screenshot_path = os.path.join(SCREENSHOTS_DIR, "error_state.png")
            page.screenshot(path=error_screenshot_path)
            print(f"❌ Error during verification: {e}")
            print(f"  - Error screenshot saved to: {error_screenshot_path}")
            raise e
        finally:
            browser.close()
        print("=== VERIFICATION COMPLETE ===")

if __name__ == "__main__":
    run_verification()
