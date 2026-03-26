from playwright.sync_api import Page, expect
import re # Add this at the top of your file



class poshmarkFeed:

    def __init__(self,page: Page):
        self.page = page

        #locators
        self.feed_sold_tag = page.locator(".icon.tile__inventory-tag.sold-tag")
        self.feed_search_title = page.locator(".search__title").filter(has_text="Search results for : ")
        self.feed_new_listing_tag= page.get_by_text("New Listings")
        self.feed_unit = page.locator(".feed__unit")
        self.feed_image = page.locator(".feed__unit__content .img__container img")
        self.feed_like_button = page.locator(".icon.heart-black-empty")
        self.feed_unlike_button = page.locator(".icon.liked")
        self.feed_search_title = page.locator(".search__title").filter(has_text="Search results for : ")
        self.price_all_prices = page.locator('label[data-test="checkbox-label"]', has_text="All Prices")
        self.price_under_25 = page.locator('label[data-test="checkbox-label"]', has_text="Under $25")
        self.price_25_to_50 = page.locator('label[data-test="checkbox-label"]', has_text="$25 - $50")
        self.price_50_to_100 = page.locator('label[data-test="checkbox-label"]', has_text="$50 - $100")
        self.price_100_to_250 = page.locator('label[data-test="checkbox-label"]', has_text="$100 - $250")
        self.price_250_to_500 = page.locator('label[data-test="checkbox-label"]', has_text="$250 - $500")
        self.price_over_500 = page.locator('label[data-test="checkbox-label"]', has_text="Over $500")



    def get_all_items_price(self) -> list[float]:
        price_elements = self.page.locator("span.p--t--1.fw--bold").all_inner_texts()

        cleaned_price = []
        for text in price_elements:
            if not "$" in text  :
                continue
            cleaned_price.append(float(text.replace("$", "").replace(",", "").strip()))
        
        return cleaned_price



    def click_filter(self, category: str, option: str):

        filter_category = category.lower()
        filter_option = option.lower()
        
        try:
            # BRAND FILTER
            if category == "Brand" or category == "Price":
                self.page.get_by_placeholder("Search brands...").fill(option)
                self.page.locator('label[class="form__label--check"]', has_text=option).click()

            # PRICE & SIZE FILTER
            elif category == "Price" or category == "Size":
                self.page.locator('[data-test="checkbox-label"', has_text=option).click()

            # SHIPPING, CONDITION, AND AVAILABILITY FILTERS
            elif category == "Shipping" or category == "Condition" or category == "Availability":
                Target = self.page.locator('label[data-test="radio-highlight"]').get_by_text(option, exact=True)

            
            # COLOR FILTER
            elif category == "Color":   
                self.page.locator(f'[data-et-prop-content="{option}"]').click()

            else:
                raise ValueError(f"❌ Filter category '{category}' not recognized. Use 'brand', 'size', 'price', 'shipping', 'condition', 'availability', or 'color'.")
            current_classes = target.get_attribute("class") or ""
            if "fw--med" not in current_classes:
                target.click()
            else:
                pass

            self.page.wait_for_timeout(500)


        except Exception as e:              
            raise Exception(f"Failed to apply filter '{option}' for category '{category}'. Error: {e}")

    

    def make_filter_visible(self,filter_name: str, ):

        category = self.page.locator('.toggle__header', has_text=filter_name)
        opened_category = self.page.locator('.toggle__header.show', has_text=filter_name)

        category.scroll_into_view_if_needed()

        if not opened_category.is_visible():
            category.click()
            self.page.wait_for_timeout(500)

    def return_filter(self,text_name: str):
        return self.page.get_by_label(text_name)
    
    def force_like_first_listing(self):

        first_lisiting = self.feed_unit.first
        first_like_button = self.feed_like_button.first
        first_unlike_button = self.feed_unlike_button.first
        first_lisiting.scroll_into_view_if_needed()
        #clicking like button can sometimes fail if the listing is already liked, so we check for that and unlike first if needed before liking
        if not first_like_button.is_visible(timeout=3000):	
            first_unlike_button.click()
            self.page.wait_for_timeout(2000)
            first_like_button.click()			
        else:
            first_like_button.click()