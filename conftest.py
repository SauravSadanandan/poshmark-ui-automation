import pytest
from playwright.sync_api import sync_playwright
import os

'''
this function runs at the start of the pytest session and checks if the authentication state file exists. 
If it doesn't, it launches a browser window for the user to manually log in and complete any OTP verification. 
Once the user successfully logs in and the feed loads, it saves the authentication state to a JSON file for future use.
'''
STATE_FILE = "other_scripts/posh_login.json"


def pytest_sessionstart(session):
    
    # checking if auth state exists, if not we need to log in manually
    if not os.path.exists(STATE_FILE):
        print("\n[Setup] No auth state found. Launching browser for manual OTP entry...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
            context = browser.new_context()
            page = context.new_page()


            # Autofill login credentials to save you time, but the user must complete the OTP verification manually in the browser window.
            page.goto("https://poshmark.com/login", wait_until="domcontentloaded", timeout=60000)
            email_field = page.get_by_placeholder("Username or Email")
            email_field.click()
            email_field.press_sequentially("sauravforapps@gmail.com", delay=150)

            password_field = page.get_by_placeholder("Password")
            password_field.click()
            password_field.press_sequentially("test123", delay=150)
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Login").click()
            print("\n Please log in and complete the OTP verification in the browser window.")
            
            try:
            # The script automatically waits for the feed to load. No manual input needed!
                page.wait_for_selector(".feed__unit__header",state="visible", timeout=0)
                
                # If the script finds the feed unit, it instantly saves the state.
                context.storage_state(path="other_scripts/posh_login.json")
                print(f"\n Authentication successful! State saved to {STATE_FILE}.")

            except Exception as e:
                print("\n❌ Automation Failed.")
                print(f"Error details: {e}")          

            browser.close()

            pytest.exit("\n❌ CRITICAL ERROR: Authentication failed or was aborted. 'posh_login.json' was not created. Aborting all tests to prevent cascading failures.")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": STATE_FILE,
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": ["--disable-blink-features=AutomationControlled"]
    }


'''
This function adds custom command-line options to pytest, allowing users to specify the environment, search item, 
and filter criteria when running tests.
'''
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help = "Choose environment: qa or prod"
        )
    
    parser.addoption(
        "--item",
        action="store",
        default="Nike Shoes",
        help = "Choose item to search for"
        )
    
    parser.addoption(
        "--filter_by",
        action="store",
        default="availability",
        help = "Choose filter category"
        )
    
    parser.addoption(
        "--filter_with",
        action="store",
        default="Available Items",
        help = "Choose filter within category"
        )

'''
these fixtures modify the browser context and launch arguments to include the authentication state saved from the manual login process, 
as well as set a realistic user agent and viewport size. This ensures that all tests run with the authenticated session and mimic a real user's browser environment.
'''

@pytest.fixture(scope="session")
def base_url(request):
    #Return the base URL based on the selected environment.
    env_choice = request.config.getoption("--env")

    if env_choice == "qa":
        return "https://poshmark.com/feed"
    elif env_choice == "prod":
        return "https://poshmark.com/feed"
    else:
        raise ValueError(f"Unknown environment: {env_choice}")

@pytest.fixture(scope="session")
def search_item(request):
    #Choose item to search for.
    return request.config.getoption("--item")


@pytest.fixture(scope="session")
def filter_category(request):
    #Choose filter category.
    return request.config.getoption("--filter_by")

@pytest.fixture(scope="session")
def filter_option(request):
    #Choose filter within category.
    return request.config.getoption("--filter_with")
