from playwright.sync_api import Page, expect
import pytest
from pages.poshmark_feed_page import poshmarkFeed
from pages.poshmark_header_page import poshmarkHeader

pytestmark = pytest.mark.regression

@pytest.fixture
def setup_poshmark(page: Page, base_url: str):
    page.goto(base_url, wait_until="domcontentloaded")
    return poshmarkFeed(page), poshmarkHeader(page)

@pytest.mark.parametrize("search_item", [
    ("Nike"),
    ("Puma" ),
    ("Jacket"),
    ("Watch" ) 
])

def test_price_filter(setup_poshmark, page: Page, search_item: str, ):
    
    feed_page, header_page = setup_poshmark
    
    header_page.item_search(search_item)
    feed_page.feed_search_title.wait_for(state="visible", timeout=5000)
    expect(feed_page.feed_search_title).to_be_visible()
    expect(feed_page.feed_search_title).to_have_text(f"Search results for : {search_item}")