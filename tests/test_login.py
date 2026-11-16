import re

import pytest
from playwright.sync_api import expect


@pytest.mark.no_auth
@pytest.mark.smoke
def test_valid_login_lands_on_inventory(login_page, sauce_credentials):
    login_page.open()
    login_page.login(*sauce_credentials)

    expect(login_page.page).to_have_url(re.compile(r".*/inventory.html$"))
    expect(login_page.page.get_by_text("Products", exact=True)).to_be_visible()


@pytest.mark.no_auth
@pytest.mark.parametrize(
    ("username", "password", "expected_error"),
    [
        (
            "locked_out_user",
            None,
            "Epic sadface: Sorry, this user has been locked out.",
        ),
        ("", None, "Epic sadface: Username is required"),
        (None, "", "Epic sadface: Password is required"),
    ],
)
@pytest.mark.regression
def test_invalid_login_shows_validation_error(
    login_page, sauce_credentials, username, password, expected_error
):
    login_page.open()
    login_page.login(
        username if username is not None else sauce_credentials[0],
        password if password is not None else sauce_credentials[1],
    )

    expect(login_page.error_message).to_have_text(expected_error)
