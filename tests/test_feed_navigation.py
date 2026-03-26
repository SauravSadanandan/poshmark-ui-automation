from playwright.sync_api import Page, expect
import pytest
import re
from pages.poshmark_feed_page import poshmarkFeed
from pages.poshmark_listing_page import poshmarkListing

pytestmark = pytest.mark.smoke

def test_feed_navigation(page : Page, base_url: str):
    feed_page = poshmarkFeed(page)
    listing_page = poshmarkListing(page)
    
    page.goto(base_url,wait_until="domcontentloaded")
    feed_page.feed_image.first.click(force=True)
    expect(page).to_have_url(re.compile(r".*/listing/.*"))
    expect(listing_page.listing_image.first).to_be_visible()
    expect(listing_page.listing_buy_now_button.first).to_be_visible()