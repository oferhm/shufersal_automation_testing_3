# fixtures/browser_fixtures.py
# ──────────────────────────────────────────────────────────────────────────────
# Fixtures — Pytest fixtures that manage browser lifecycle.
#
# HOW FIXTURES WORK:
#   A @pytest.fixture function is injected automatically into any test that
#   declares it as a parameter. The `yield` separates setup (before) from
#   teardown (after) — teardown runs even if the test fails.
#
# SCOPES:
#   scope="session"  → one browser process for the entire test run (fast)
#   scope="function" → fresh context/page per test (full isolation)
# ──────────────────────────────────────────────────────────────────────────────

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from pages.home_page import HomePage


# ── Low-level browser infrastructure ─────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance(request):
    headed = request.config.getoption("--headed")    # ← built-in pytest-playwright flag
    slow_mo = request.config.getoption("--slowmo", default=0)  # ← custom flag

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=not headed,   # ← flips headed → headless
            slow_mo=slow_mo,
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser_instance) -> BrowserContext:
    """
    Create a fresh browser CONTEXT per test.

    A context is like an incognito window — completely separate cookies,
    localStorage, and session state. This means each test starts clean
    even though they share the same browser process.
    """
    ctx: BrowserContext = browser_instance.new_context(
        viewport={"width": 1440, "height": 900},
        locale="he-IL",          # Israeli locale — helps with Hebrew site rendering
        timezone_id="Asia/Jerusalem",
    )
    yield ctx
    ctx.close()                  # ← teardown: runs after each individual test


@pytest.fixture(scope="function")
def page(context) -> Page:
    """Open a single tab (Page) inside the isolated context."""
    tab: Page = context.new_page()
    yield tab
    tab.close()


# ── Page Object fixture ───────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def home_page(page) -> HomePage:
    """
    Inject a HomePage instance into any test that requests it.

    The test only sees a high-level HomePage — no raw Playwright API.
    Usage:
        def test_something(self, home_page):
            home_page.open().search_for("חלב")
    """
    return HomePage(page)
