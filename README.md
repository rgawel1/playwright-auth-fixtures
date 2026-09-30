# Playwright Auth Fixtures

This project demonstrates a reusable pytest + Playwright authentication pattern for web applications.

The main idea is:
- log in once in a shared browser context
- reuse that authenticated context in tests
- configure the user and URL externally via environment variables or test parameters

## Project structure

- `conftest.py` – reusable Playwright fixtures and login helper
- `tests/test_auth_flow.py` – example tests using the authenticated context
- `.env.example` – environment variables for app URL and credentials
- `requirements.txt` – project dependencies

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

Copy the env file and adjust the values:

```bash
cp .env.example .env
```

## Usage

The key fixture is `authenticated_context` and it logs in once per suite. Tests can then open new pages from that same authenticated context rather than logging in again every time.

```python
def test_dashboard(authenticated_page):
    authenticated_page.goto("https://example.com/dashboard")
    assert authenticated_page.url.startswith("https://example.com")
```

Multiple users can be supplied through parametrization:

```python
import pytest

@pytest.mark.parametrize(
    "auth_config",
    [
        {"base_url": "https://example.com", "username": "admin", "password": "admin123"},
        {"base_url": "https://example.com", "username": "user", "password": "user123"},
    ],
    indirect=True,
)
def test_login_variants(authenticated_page):
    assert authenticated_page.url.startswith("https://example.com")
```

## Why this pattern is good

- no repeated login in every test
- one authenticated session per suite
- easy to configure for different URLs and users
- easy to adapt to any login form or SSO flow
