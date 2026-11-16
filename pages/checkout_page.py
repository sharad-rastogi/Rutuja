from playwright.sync_api import Locator, Page


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.error_message = page.get_by_test_id("error")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.complete_header = page.get_by_role(
            "heading", name="Thank you for your order!"
        )

    def submit_customer_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)
        self.continue_button.click()

    def finish_order(self) -> None:
        self.finish_button.click()

    @staticmethod
    def amount(locator: Locator) -> str:
        return locator.inner_text().split("$", maxsplit=1)[1]
