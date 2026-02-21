from playwright.sync_api import Page
class PoshmarkSearchPage:

	def __init__(self,page: Page):
		self.page = page

		#locators
		self.search_bar = page.get_by_placeholder("Search Listings")
		self.search_title = page.locator(".search__title")
		self.sold_tag = page.locator(".icon.tile__inventory-tag.sold-tag")

	def item_search(self,item_name: str):
		self.search_bar.fill(item_name)
		self.search_bar.press("Enter")

	def apply_filter(self,filter_name: str, filter_option: str):

		category = self.page.get_by_text(filter_name)
		option  = self.page.get_by_text(filter_option)

		if not option.is_visible():
			category.click()

		option.click()


	def return_filter(self,text_name: str):
		return self.page.get_by_text(text_name)