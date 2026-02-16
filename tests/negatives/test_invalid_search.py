import json
from pathlib import Path

import pytest

from pages.shufersal.home_page import ShufersalHomePage

from pages.shufersal.shopping_page import ShufersalSearchResultsPage

DATA_PATH = Path(__file__).parent.parent / "data" / "product_data.json"
with open(DATA_PATH, encoding="utf-8") as f:
    products_data = json.load(f)

valid_products = products_data["valid_product_info"]
invalid_products = products_data["invalid_product_info"]


@pytest.mark.asyncio
@pytest.mark.parametrize("product", invalid_products)
async def test_invalid_search(page_with_device, product) -> None:
    page, is_mobile = page_with_device
    home = ShufersalHomePage(page)
    search_results_page = ShufersalSearchResultsPage(page)

    await home.goto()
    await home.header.search(product['name'])

    await search_results_page.validate_no_results()
