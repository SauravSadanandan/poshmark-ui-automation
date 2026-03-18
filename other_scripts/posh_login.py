from playwright.sync_api import sync_playwright

def poshmark_login():
    with sync_playwright() as p:
        # Launching with stealth arguments to hide that this is an automated browser
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        
        # Adding a realistic User-Agent makes the browser look like a standard Google Chrome user
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("Navigating to Poshmark...")
        page.goto("https://poshmark.com/login", wait_until="domcontentloaded", timeout=60000)
        
        print("Typing credentials...")
        email_field = page.get_by_placeholder("Username or Email")
        email_field.click()
        email_field.press_sequentially("sauravforapps@gmail.com", delay=100)
        
        password_field = page.get_by_placeholder("Password")
        password_field.click()
        password_field.press_sequentially("test123", delay=100)
        
        page.wait_for_timeout(1000)
        print("Clicking Login...")
        page.get_by_role("button", name="Login").click()

        print("Waiting up to 30 seconds for the feed to appear...")
        try:
            # The script automatically waits for the feed to load. No manual input needed!
            page.wait_for_selector(".feed__unit__header", timeout=30000)
            
            # If the script finds the feed unit, it instantly saves the state.
            context.storage_state(path="posh_login.json")
            print("✅ SUCCESS: Fully automated login complete! State saved to posh_login.json")
            
        except Exception as e:
            print("\n❌ Automation Failed.")
            print("Reason: Poshmark likely threw a Captcha or security check that blocked the automated login.")
            print(f"Error details: {e}")
            
        browser.close()

if __name__ == "__main__":
    poshmark_login()