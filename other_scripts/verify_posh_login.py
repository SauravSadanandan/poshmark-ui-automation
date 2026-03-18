from playwright.sync_api import sync_playwright

def test_poshmark_loginstate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            storage_state="posh_login.json",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Navigating to Poshmark Feed...")
        
        page.goto("https://poshmark.com/feed", wait_until="domcontentloaded", timeout=5000)

        try:
            page.wait_for_selector(".feed__unit__header", timeout=15000)
            print("✅ SUCCESS: state file is working")
        except Exception as e:
            print("❌ FAILED: state file failed, please run posh_login.py to recreate login state")
            
        browser.close()

if __name__ == "__main__":
    test_poshmark_loginstate()