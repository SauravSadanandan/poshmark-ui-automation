# Poshmark UI Automation Project

This is a UI automation project I built to test the Poshmark website. I created this to practice writing clean, reusable test code using Python and Playwright.

## Tools Used
* **Python**
* **Playwright** (for browser automation)
* **Pytest** (for running the tests)
* **Page Object Model (POM)** (for organizing the code)

## What Makes This Code Special

* **Organized Code (POM):** I separated the test data from the website actions. The `tests` file only gives commands, and the `pages` file handles the actual clicking and typing.
* **Dynamic Filter Method:** Instead of writing a separate method for every single filter on Poshmark (like Brands, Size, Condition), I wrote one dynamic `apply_filter()` method. It can click any filter category and option just by passing in the text.
* **Smart Clicking Logic:** The code is smart enough to check if a drop-down menu is hidden. If the option isn't visible, it automatically clicks the category header to open the menu first.
* **Reliable Locators:** I used Playwright's `exact=True` for text matching so the tests don't accidentally click the wrong buttons.

## Project Files
```text
AutomationProject/
├── pages/
│   └── poshmark_search_page.py    # Holds the locators and clicking actions
├── tests/
│   └── test_poshmark_search.py    # Holds the actual test steps and assertions
├── conftest.py                    # Setup file for Pytest
└── README.md                      # This file
