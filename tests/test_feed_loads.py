from playwright.sync_api import Page, expect
import pytest
from pages.poshmark_feed_page import poshmarkFeed

pytestmark = pytest.mark.smoke

def test_feed_smoke(page : Page, base_url: str):
    current_test = poshmarkFeed(page)
    page.goto(base_url)

    
    expect(current_test.first_new_listing).to_be_visible()
    expect(current_test.first_feed_unit).to_be_visible()
    expect(current_test.first_feed_image).to_be_visible()


    