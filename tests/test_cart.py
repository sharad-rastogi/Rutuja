import pytest
from playwright.sync_api import expect


@pytest.mark.regression
def test_removing_cart_item_persists_on_inventory(
    inventory_page, cart_page
):
    removed_product = "Sauce Labs Backpack"
    remaining_product = "Sauce Labs Bike Light"

    inventory_page.page.goto("/inventory.html")
    inventory_page.add_to_cart(removed_product)
    inventory_page.add_to_cart(remaining_product)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.open_cart()
    cart_page.remove_item(removed_product)
    expect(cart_page.item_names).to_have_text([remaining_product])
    expect(cart_page.cart_badge).to_have_text("1")

    cart_page.continue_shopping()
    expect(
        inventory_page.product_card(removed_product).get_by_role(
            "button", name="Add to cart"
        )
    ).to_be_visible()
    expect(
        inventory_page.product_card(remaining_product).get_by_role(
            "button", name="Remove"
        )
    ).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text("1")
