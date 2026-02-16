import re

import allure


class ProductCard:
    def __init__(self, grid_locator, name, manufacturer, volume, is_mobile=False):
        self.product_name = name
        self.manufacturer = manufacturer
        self.volume = volume
        self.product_card = (
            grid_locator
            .locator("li")
            .filter(has_text=name)
            .filter(has_text=manufacturer)
            .filter(has_text=volume)
            .first
        )
        self.brand = self.product_card.locator("div.brand-name")
        self.add_button = self.product_card.locator("button.btn.js-add-to-cart.js-enable-btn.miglog-btn-add")
        self.product_price = self.product_card.locator("span.price").locator("span.number")
        self.product_out_of_stock = self.product_card.get_by_text("חסר במלאי").nth(0)
        self.is_mobile = is_mobile
        self.mobile_add_button = self.product_card.locator("button.btn.miglog-btn-add").nth(1)

    async def add_to_cart(self):
        if self.is_mobile:
            await self.mobile_add_button.click()
            await self.product_card.locator("ul").get_by_text("1").nth(0).click()
        else:
            await self.add_button.click()

    async def get_price(self):
        price = await self.product_price.text_content()
        return str(float(re.sub(r"[^\d.]", "", price)))

    async def simulate_out_of_stock(self):
        with allure.step(f"Simulate product {self.product_name} as out of stock"):
            await self.product_card.evaluate("""
                (card) => {
                    let outOfStockMsg = card.querySelector('.miglog-prod-outOfStock-msg');
                    if (!outOfStockMsg) {
                        outOfStockMsg = document.createElement('div');
                        outOfStockMsg.className = 'miglog-prod-outOfStock-msg';
                        outOfStockMsg.textContent = 'חסר במלאי';
                        card.appendChild(outOfStockMsg);
                    }
                    outOfStockMsg.style.display = 'block';
                    card.classList.add('out-of-stock');
                    const addButton = card.querySelector('button');
                    if (addButton) {
                        addButton.disabled = true;
                        addButton.textContent = 'לא במלאי';
                    }
                }
            """)

    def get_product_out_of_stock_locator(self):
        return self.product_out_of_stock.nth(0)
