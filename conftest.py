import os
import re
from pathlib import Path

import pytest
from playwright.sync_api import Browser, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--username",
        action="store",
        default=os.getenv("SAUCE_USERNAME"),
        help="Sauce Demo username (or set SAUCE_USERNAME).",
    )
    parser.addoption(
        "--password",
        action="store",
        default=os.getenv("SAUCE_PASSWORD"),
        help="Sauce Demo password (or set SAUCE_PASSWORD).",
    )


def pytest_configure(config: pytest.Config) -> None:
    browser_from_env = os.getenv("PLAYWRIGHT_BROWSER")
    browser_was_selected = any(
        argument == "--browser" or argument.startswith("--browser=")
        for argument in config.invocation_params.args
    )
    if browser_from_env and not browser_was_selected:
        config.option.browser = [browser_from_env]

    headed_from_env = os.getenv("PLAYWRIGHT_HEADED", "").lower()
    headless_from_env = os.getenv("PLAYWRIGHT_HEADLESS", "").lower()
    if not config.option.headed and (
        headed_from_env in {"1", "true", "yes"}
        or headless_from_env in {"0", "false", "no"}
    ):
        config.option.headed = True


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session) -> None:
    Path("reports").mkdir(exist_ok=True)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    Path("test-results").mkdir(exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def use_application_test_ids(playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return (
        pytestconfig.getoption("base_url")
        or os.getenv("SAUCE_BASE_URL")
        or pytestconfig.getini("base_url")
    )


@pytest.fixture(scope="session")
def sauce_credentials(pytestconfig: pytest.Config) -> tuple[str, str]:
    username = pytestconfig.getoption("username")
    password = pytestconfig.getoption("password")
    if not username or not password:
        raise pytest.UsageError(
            "Set SAUCE_USERNAME and SAUCE_PASSWORD or pass --username and --password."
        )
    return username, password


@pytest.fixture(scope="session")
def authenticated_storage_state(
    browser: Browser,
    base_url: str,
    sauce_credentials: tuple[str, str],
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    state_file = tmp_path_factory.mktemp("auth") / "storage_state.json"
    context = browser.new_context(
        base_url=base_url,
    )
    try:
        page = context.new_page()
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(*sauce_credentials)
        expect(page).to_have_url(re.compile(r".*/inventory.html$"))
        context.storage_state(path=state_file)
    finally:
        context.close()
    return state_file


@pytest.fixture
def browser_context_args(
    browser_context_args: dict[str, object],
    base_url: str,
    request: pytest.FixtureRequest,
) -> dict[str, object]:
    context_args = dict(browser_context_args)
    context_args["base_url"] = base_url

    if request.node.get_closest_marker("no_auth") is None:
        state_file = request.getfixturevalue("authenticated_storage_state")
        context_args["storage_state"] = str(state_file)

    return context_args


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)
