from  playwright.sync_api import sync_playwright

def test_poshmark_loginstate():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False, slow_mo=1000)
        try:
            context = browser.new_context(storage_state="posh_login.json")

        except Exception as e:
            print(f"Failed to load login state! Please run posh_login.py first. error: {e}")
            browser.close()
            return
        page = context.new_page()

        page.goto("https://poshmark.com/feed")
        page.wait_for_timeout(5000)  # Wait for potential redirects and page load
        current_url = page.url
        if "login" in current_url:
            print("Login state is invalid or expired. Please run posh_login.py to refresh it.")
        else:
            print("Login state is valid! Successfully accessed feed page.")
            print(f"Current URL: {current_url}")

        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    test_poshmark_loginstate()