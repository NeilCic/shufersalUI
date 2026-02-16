import json
from pathlib import Path

import pytest

from pages.shufersal.home_page import ShufersalHomePage
from playwright.async_api import expect

from pages.shufersal.shopping_page import ShufersalSearchResultsPage

DATA_PATH = Path(__file__).parent.parent / "data" / "product_data.json"
with open(DATA_PATH, encoding="utf-8") as f:
    products_data = json.load(f)

valid_products = products_data["valid_product_info"]


@pytest.mark.asyncio
@pytest.mark.parametrize("product", [valid_products[0]])
async def test_out_of_stock_add_to_cart(page_with_device, product) -> None:
    page, is_mobile = page_with_device
    home = ShufersalHomePage(page)
    search_results_page = ShufersalSearchResultsPage(page)

    await home.goto()
    await home.header.search(product['name'])
    product_card = await search_results_page.get_product_card(**product)
    await product_card.simulate_out_of_stock()
    await expect(product_card.get_product_out_of_stock_locator()).to_be_visible()
