from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_test_id("error")

    def open(self) -> None:
        self.page.goto("/")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
