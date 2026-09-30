import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

load_dotenv()


@dataclass(frozen=True)
class AuthConfig:
    base_url: str
    username: str
    password: str


def get_auth_config(**overrides: str) -> AuthConfig:
    return AuthConfig(
        base_url=overrides.get("base_url", os.getenv("APP_URL", "https://example.com")),
        username=overrides.get("username", os.getenv("APP_USER", "demo_user")),
        password=overrides.get("password", os.getenv("APP_PASSWORD", "demo_password")),
    )


def login_user(page: Page, config: AuthConfig) -> None:
    """
    Reusable login flow for standard username/password forms.

    Keep this logic separate from tests so it can be reused across many cases
    and easily adapted to different auth implementations.
    """
    page.goto(config.base_url)

    page.fill("input[name='username'], input[type='email'], input#username", config.username)
    page.fill("input[name='password'], input[type='password'], input#password", config.password)
    page.click("button[type='submit'], input[type='submit']")

    page.wait_for_load_state("networkidle")


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright):
    browser = playwright_instance.chromium.launch(headless=False)
    try:
        yield browser
    finally:
        browser.close()


@pytest.fixture
def auth_config(request: pytest.FixtureRequest) -> AuthConfig:
    """
    Support for:
    - env-based configuration
    - indirect parametrization in tests
    """
    if hasattr(request, "param") and request.param:
        return get_auth_config(**request.param)
    return get_auth_config()


@pytest.fixture(scope="session")
def authenticated_context(browser: Browser, auth_config: AuthConfig):
    """
    One authenticated browser context for the whole test suite.
    Login happens once here; tests only reuse it.
    """
    context = browser.new_context()
    page = context.new_page()

    login_user(page, auth_config)

    yield context

    context.close()


@pytest.fixture
def authenticated_page(authenticated_context):
    """
    Return a fresh page from the already authenticated context.
    This avoids repeating login for each test.
    """
    page = authenticated_context.new_page()
    try:
        yield page
    finally:
        page.close()
