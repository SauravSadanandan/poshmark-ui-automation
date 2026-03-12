from playwright.sync_api import Page
class poshmarkFeed:

	def __init__(self,page: Page):
		self.page = page

		#locators
		self.search_bar = page.get_by_placeholder("Search Listings")
		self.search_title = page.locator(".search__title")
		self.sold_tag = page.locator(".icon.tile__inventory-tag.sold-tag")
		self.first_new_listing = page.get_by_text("New Listings").first
		self.first_feed_unit = page.locator(".feed__unit").first
		self.first_feed_image = page.locator(".feed__unit__content picture img").first
		self.first_listing_image = page.locator(".img__container picture img").first
		self.buy_now_button = page.get_by_role("button", name="Buy Now")
		self.first_like_button = page.locator(".heart-black-empty").first
		self.first_unlike_button = page.locator(".liked").first


	def item_search(self,item_name: str):
		self.search_bar.fill(item_name)
		self.search_bar.press("Enter")

	def apply_filter(self,filter_name: str, filter_option: str):

		category = self.page.get_by_text(filter_name)
		option  = self.page.get_by_text(filter_option)

		category.scroll_into_view_if_needed()
		option.scroll_into_view_if_needed()

		if not option.is_visible():
			category.click()

		option.click()


	def return_filter(self,text_name: str):
		return self.page.get_by_text(text_name)
	
	def click_first_like(self):
		if not self.first_like_button.is_visible(timeout=2000):	
			self.first_unlike_button.click()
		else:
			self.first_like_button.click()