# Poshmark UI Automation Project 🛍️

I built this UI automation framework to test the Poshmark website. The goal was to practice writing clean, maintainable test code using **Python** and **Playwright**, while solving real-world automation problems like handling dynamic dropdowns and bypassing login screens.

## The Tools
* **Python** * **Playwright** (for fast, reliable browser automation)
* **Pytest** (for running tests and managing custom CLI arguments)
* **Page Object Model (POM)** (to keep the locators separate from the test logic)

## The Coolest Features in This Repo

Instead of just recording and playing back clicks, I wrote a few custom solutions that I'm really proud of:

* **Saved Login States:** Logging in before every single test takes way too much time. I wrote a standalone script (`other_scripts/posh_login.py`) that logs into Poshmark once and saves the browser cookies to a `json` file. The Pytest suite then injects this file so all tests start fully authenticated.
* **Dynamic Filter Engine:** Instead of hardcoding separate functions for "Filter by Brand", "Filter by Size", etc., I wrote one `apply_filter()` method. You just pass in the category and the option as text, and it figures out how to scroll, expand hidden menus, and click the right box.
* **Custom Pytest Commands:** I set up `conftest.py` with custom command-line arguments. You can trigger a test and tell it exactly what to search for right from the terminal (e.g., `pytest --item="Nike Shoes" --filter_by="Condition"`). 
* **Smart UI Toggles:** Poshmark feed items can be tricky to test because they might already be "liked" from a previous test run. I built a `force_like_first_listing` method that checks the current state of the heart icon first, ensuring the test always ends in the exact state it expects without crashing.
* **Built-in Trace Viewer:** If a test fails, `pytest.ini` is configured to automatically save a time-traveling trace file so I can debug exactly what went wrong frame-by-frame.

## Project Layout
```text
poshmark-ui-automation/
├── pages/
│   └── poshmark_feed_page.py      # Holds all locators, search logic, and filter methods
├── tests/
│   ├── test_feed_likefunc.py      # Tests the like/unlike toggle
│   ├── test_feed_loads.py         # Verifies the main feed loads correctly
│   ├── test_feed_navigation.py    # Tests clicking into a listing
│   └── test_search_and_filter.py  # Tests the search bar and dynamic filtering
├── other_scripts/
│   ├── posh_login.py              # Run this first! Generates the auth state file
│   └── verify_posh_login.py       # Quick script to check if your session is still valid
├── conftest.py                    # Pytest fixtures and custom terminal commands
└── pytest.ini                     # Registers markers (smoke, regression) and trace configs
```

**How to Run This on Your Computer**

If you want to download this code and run the automation on your own machine, follow these steps:

**1. Download the code**
```bash
git clone [https://github.com/SauravSadanandan/poshmark-ui-automation.git](https://github.com/SauravSadanandan/poshmark-ui-automation.git)
cd poshmark-ui-automation
```

**2. Install what you need**
Make sure you have Python installed, then run these commands to get the testing tools:
```bash
pip install pytest playwright
playwright install
```

**3. Run the test**
This command will open a visible browser so you can watch the automation search and filter in real-time:
```bash
pytest tests/test_poshmark_search.py --headed
```
