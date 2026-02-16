from playwright.async_api import expect

from pages.shufersal.components.header import Header
from pages.shufersal.components.product_card import ProductCard
from pages.shufersal.components.shopping_cart import ShoppingCart


class ShufersalSearchResultsPage:
    def __init__(self, page):
        self.page = page
        self.header = Header(page)
        self.shopping_cart = ShoppingCart(page)
        self.no_search_result = page.locator(".noSearchResult").nth(0)

        self.grid = page.locator("ul#mainProductGrid")

    async def get_product_card(self, name, manufacturer, volume, is_mobile=False):
        return ProductCard(self.grid, name, manufacturer, volume, is_mobile)

    # todo remove
    # async def fill_in_delivery_details(self, year, month, day, hour="20:00", city="תל אביב - יפו", street="דיזנגוף", num="1"):
    #     city_input_bar = self.page.locator("input#cityInput")
    #     expect(city_input_bar).to_be_visible(timeout=60000)
    #     expect(city_input_bar).to_be_enabled()
    #     await city_input_bar.click()
    #     await city_input_bar.fill(city)
    #     await self.page.get_by_text(city).click()
    #     await self.page.locator("input#streetInput").fill(street)
    #     await self.page.get_by_text("דיזנגוף", exact=True).click()
    #     await self.page.get_by_role("textbox", name="מספר").fill(num)
    #     await self.page.get_by_role("button", name="להמשך").click()
    #     date_options = self.page.locator("div.slick-track")
    #     time_options = date_options.locator(f"div#day_{year}{month}{day}").locator('..')
    #     await time_options.locator(f"label[aria-label*='{hour}']").click()
    #     await self.page.get_by_role("button", name="שמירה").click()

    async def validate_no_results(self):
        await expect(self.no_search_result).to_be_visible()

    def get_out_of_stock_product(self):
        return self.grid.locator(".product-card.out-of-stock:visible").first
