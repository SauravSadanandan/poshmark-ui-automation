import re
from playwright.sync_api import Page, expect

def test_poshmark_search(page : Page, base_url: str):
	page.goto(base_url)
	page.get_by_placeholder("Search Listings").fill("Nike Shoes")
	page.get_by_placeholder("Search Listings").press("Enter")	

	#verifing if Nike shoes is visible
	expect(page.locator(".search__title")).to_contain_text("Nike shoes", ignore_case=True)

	availability_option = page.get_by_text("Available Items", exact=True)

	if not availability_option.is_visible():
		page.get_by_text("availability").click()

	availability_option.click()
	expect(availability_option).to_be_visible()

	#checking if sold label is not visible, which means only available items are listed
	expect(page.locator(".icon.tile__inventory-tag.sold-tag")).to_have_count(0)