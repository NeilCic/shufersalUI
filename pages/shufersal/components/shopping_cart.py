import re

import allure


class ShoppingCart:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("input[type='search']")
        self.cart_button = page.locator("[data-automation-id='cart-button']")
        self.cart_counter = page.locator("#cartTotalItems")
        self.delivery_cost = page.locator("div.wrapperShipingText").locator("span.infoSubText")
        self.total_cost = page.locator("div.price").locator("span.currency.currencyBtnToggle")

    async def count_cart_items(self):
        return await self.cart_counter.text_content()

    async def get_cart_products(self):
        cart_products_locator = self.page.locator("section.miglog-prod-subGroup")
        count = await cart_products_locator.count()
        cart_products_info = []
        for i in range(count):
            item = cart_products_locator.nth(i)
            title = await item.locator("h3.miglog-text3.miglog-prod-name ").text_content()
            quantity_raw = await item.locator("p.miglog-text3.miglog-prod-qt.miglog-minicart-visible-only").text_content()
            price_raw = await item.locator("p.miglog-text2.miglog-prod-totalPrize").text_content()

            quantity = int(re.sub(r"[\D]", "", quantity_raw))
            price = str(float(re.sub(r"[^\d.]", "", price_raw)))

            cart_products_info.append({
                'title': " ".join(title.split()),
                'quantity': quantity,
                'price': price
            })

            return cart_products_info

    async def open_cart(self):
        await self.cart_button.click()

    @allure.step("Click pay for cart")
    async def pay_for_cart(self):
        await self.page.locator("a").filter(has_text="לתשלום").click()
