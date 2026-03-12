from playwright.sync_api import Page, expect
import pytest
import re
from pages.poshmark_feed_page import poshmarkFeed
pytestmark = pytest.mark.smoke

def test_feed_navigation(page : Page, base_url: str):
    current_test = poshmarkFeed(page)
    page.goto(base_url)
    current_test.first_feed_image.click()
    expect(page).to_have_url(re.compile(r".*/listing/.*"))
    expect(current_test.first_listing_image).to_be_visible()
    expect(current_test.buy_now_button).to_be_visible()