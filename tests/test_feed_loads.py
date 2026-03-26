from playwright.sync_api import Page, expect
import pytest
from pages.poshmark_feed_page import poshmarkFeed

pytestmark = pytest.mark.smoke

def test_feed_smoke(page : Page, base_url: str):
    feed_page = poshmarkFeed(page)
    page.goto(base_url,wait_until="domcontentloaded")

    
    expect(feed_page.feed_new_listing_tag.first).to_be_visible()
    expect(feed_page.feed_unit.first).to_be_visible()
    expect(feed_page.feed_image.first).to_be_visible()


    