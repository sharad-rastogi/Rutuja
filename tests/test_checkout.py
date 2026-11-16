from decimal import Decimal

import pytest
from playwright.sync_api import expect


BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_two_item_checkout_calculates_total(inventory_page, cart_page, checkout_page):
    inventory_page.page.goto("/inventory.html")
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.open_cart()
    expect(cart_page.item_names).to_have_text([BACKPACK, BIKE_LIGHT])
    cart_page.checkout()
    checkout_page.submit_customer_information("Rutuja", "Raikar", "411001")

    subtotal = Decimal(checkout_page.amount(checkout_page.subtotal))
    tax = Decimal(checkout_page.amount(checkout_page.tax))
    total = Decimal(checkout_page.amount(checkout_page.total))
    assert subtotal + tax == total

    checkout_page.finish_order()
    expect(checkout_page.complete_header).to_be_visible()


@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "expected_error"),
    [
        ("", "Raikar", "411001", "Error: First Name is required"),
        ("Rutuja", "", "411001", "Error: Last Name is required"),
        ("Rutuja", "Raikar", "", "Error: Postal Code is required"),
    ],
)
@pytest.mark.regression
def test_checkout_requires_customer_information(
    inventory_page,
    cart_page,
    checkout_page,
    first_name,
    last_name,
    postal_code,
    expected_error,
):
    inventory_page.page.goto("/inventory.html")
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()
    cart_page.checkout()
    checkout_page.submit_customer_information(first_name, last_name, postal_code)

    expect(checkout_page.error_message).to_have_text(expected_error)
