from playwright.sync_api import sync_playwright

def poshmark_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto("https://poshmark.com/login")
            page.locator('[data-test="login-form-username-email-field-text-input"]').fill("sauravforapps@gmail.com")
            page.locator('[data-test="login-form-password-field-text-input"]').fill("test123")
            page.get_by_role("button", name="Login").click()

        except Exception as e:
            print(f"Auto-fill failed! Please try manually.  error: {e}")
    

        page.wait_for_selector('[data-test="text-input"]')

        page.wait_for_url("**/feed**", timeout=60000)  # Wait for successful login and redirect
        page.context.storage_state(path="posh_login.json")
        print("Login successful! Storage state saved to posh_login.json")
        browser.close()

if __name__ == "__main__":
    poshmark_login()