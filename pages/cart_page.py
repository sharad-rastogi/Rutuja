from playwright.sync_api import Locator, Page


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping_button = page.get_by_role(
            "button", name="Continue Shopping"
        )

    def item(self, product_name: str) -> Locator:
        return self.page.get_by_test_id("inventory-item").filter(
            has_text=product_name
        )

    def remove_item(self, product_name: str) -> None:
        self.item(product_name).get_by_role("button", name="Remove").click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def checkout(self) -> None:
        self.checkout_button.click()
