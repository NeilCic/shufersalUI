import pytest

from pages.shufersal.home_page import ShufersalHomePage


@pytest.mark.asyncio
async def test_special_char_product(page_with_device, product_name: str = "!@#$%^&*") -> None:
    page, is_mobile = page_with_device
    home = ShufersalHomePage(page)
    await home.goto()

    dialog_message = None

    async def handle_dialog(dialog):
        nonlocal dialog_message
        dialog_message = dialog.message
        await dialog.accept()
    page.on("dialog", handle_dialog)

    await home.header.search(product_name)
    assert dialog_message == "הוזן תו לא חוקי"
