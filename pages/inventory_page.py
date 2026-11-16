from playwright.sync_api import Locator, Page


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_names = page.get_by_test_id("inventory-item-name")
        self.product_prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")

    def product_card(self, product_name: str) -> Locator:
        return self.page.get_by_test_id("inventory-item").filter(has_text=product_name)

    def add_to_cart(self, product_name: str) -> None:
        self.product_card(product_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, product_name: str) -> None:
        self.product_card(product_name).get_by_role("button", name="Remove").click()

    def open_cart(self) -> None:
        self.cart_link.click()
