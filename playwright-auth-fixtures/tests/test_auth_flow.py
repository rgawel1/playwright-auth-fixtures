import pytest


@pytest.mark.parametrize(
    "auth_config",
    [
        {"base_url": "https://example.com", "username": "admin", "password": "admin123"},
        {"base_url": "https://example.com", "username": "user", "password": "user123"},
    ],
    indirect=True,
)
def test_authenticated_user_can_open_dashboard(authenticated_page):
    authenticated_page.goto("https://example.com/dashboard")
    assert authenticated_page.url.startswith("https://example.com")


def test_authenticated_user_can_open_account(authenticated_page):
    authenticated_page.goto("https://example.com/account")
    assert authenticated_page.url.startswith("https://example.com")
