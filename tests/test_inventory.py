import pytest
from playwright.sync_api import expect


@pytest.mark.regression
@pytest.mark.parametrize(
    ("sort_option", "expected_names"),
    [
        (
            "Price (low to high)",
            [
                "Sauce Labs Onesie",
                "Sauce Labs Bike Light",
                "Sauce Labs Bolt T-Shirt",
                "Test.allTheThings() T-Shirt (Red)",
                "Sauce Labs Backpack",
                "Sauce Labs Fleece Jacket",
            ],
        ),
        (
            "Name (Z to A)",
            [
                "Test.allTheThings() T-Shirt (Red)",
                "Sauce Labs Onesie",
                "Sauce Labs Fleece Jacket",
                "Sauce Labs Bolt T-Shirt",
                "Sauce Labs Bike Light",
                "Sauce Labs Backpack",
            ],
        ),
    ],
)
def test_products_sort_in_requested_order(inventory_page, sort_option, expected_names):
    inventory_page.page.goto("/inventory.html")
    inventory_page.sort_dropdown.select_option(label=sort_option)

    expect(inventory_page.product_names).to_have_text(expected_names)
