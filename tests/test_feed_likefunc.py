from playwright.sync_api import Page, expect
import pytest
from pages.poshmark_feed_page import poshmarkFeed
pytestmark = pytest.mark.smoke

@pytest.fixture
def setup_poshmark(page: Page, base_url: str):
    page.goto(base_url, wait_until="domcontentloaded")
    return poshmarkFeed(page)


def test_feed_likefunc(setup_poshmark, page :Page, base_url: str):
    current_test = setup_poshmark
    page.goto(base_url, wait_until="domcontentloaded")

    expect(current_test.feed_unit.first).to_be_visible()
    expect(current_test.feed_image.first).to_be_visible()
    current_test.force_like_first_listing()
    expect(current_test.feed_unlike_button.first).to_be_visible()