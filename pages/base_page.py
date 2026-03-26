# pages/base_page.py
# ──────────────────────────────────────────────────────────────────────────────
# BasePage — Shared foundation for every Page Object in the project.
#
# DESIGN PRINCIPLE:
#   All raw Playwright API calls live here.
#   Page Objects inherit BasePage and only expose high-level user actions.
#   Tests never call Playwright directly — they only call page object methods.
#
# BENEFITS:
#   • One place to adjust timeouts, add logging, or take screenshots on failure.
#   • Page objects stay clean — no boilerplate repeated across files.
#   • Tests read like plain English user stories.
# ──────────────────────────────────────────────────────────────────────────────

from playwright.sync_api import Page, expect
from utils.constants import Timeouts


class BasePage:
    """
    Abstract base class inherited by all page objects.

    Every page object must:
      1.  Inherit BasePage
      2.  Call super().__init__(page) in its __init__
      3.  Define its selectors as private class constants
      4.  Expose descriptive action/query methods
    """

    def __init__(self, page: Page) -> None:
        # The single Playwright Page (browser tab) shared across all pages
        # in one test run. Stored here so inherited methods can use it.
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        """Go to a URL and wait for the network to settle."""
        self.page.goto(url, wait_until="domcontentloaded", timeout=Timeouts.NAVIGATION)

    def get_current_url(self) -> str:
        return self.page.url

    # ── Interactions ──────────────────────────────────────────────────────────

    def click(self, selector: str, timeout: int = Timeouts.DEFAULT) -> None:
        """Wait for element to be visible, then click it."""
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        self.page.locator(selector).click()

    def click_first_element(self, selector: str, timeout: int = Timeouts.DEFAULT) -> None:
        """Wait for the first element matching the selector to be visible, then click it."""
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
        self.page.locator(selector).first.click()

    def fill(self, selector: str, text: str, timeout: int = Timeouts.DEFAULT) -> None:
        """Clear the field and type text into it."""
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        self.page.locator(selector).fill(text)

    def hover(self, selector: str, timeout: int = Timeouts.DEFAULT) -> None:
        """
        Wait for element to be visible, then move the mouse over it.

        WHY: Some menus, tooltips, and dropdowns only appear on hover —
             they are not in the DOM until the cursor is over the trigger.
             Using wait_for(visible) first avoids hovering on a ghost element
             that hasn't rendered yet.
        """
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        self.page.locator(selector).hover()

    def press_key(self, selector: str, key: str) -> None:
        """Press a keyboard key on a focused element (e.g. 'Enter')."""
        self.page.locator(selector).press(key)

    # ── Queries ───────────────────────────────────────────────────────────────

    def get_text(self, selector: str, timeout: int = Timeouts.DEFAULT) -> str:
        """Return the visible text content of a single element."""
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
        return self.page.locator(selector).inner_text().strip()
    
    def get_text_of_first_element(self, selector: str, timeout: int = Timeouts.DEFAULT) -> str:
        """Return the visible text content of the first element matching the selector."""
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
        return self.page.locator(selector).first.inner_text().strip()

    def get_all_texts(self, selector: str, timeout: int = Timeouts.DEFAULT) -> list[str]:
        """
        Return a list of text strings for every element matching the selector.

        WHY: Search results and cart items produce multiple elements with the
             same class — we need all of them for verification.
        """
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
        return [
            loc.inner_text().strip()
            for loc in self.page.locator(selector).all()
        ]

    def get_input_value(self, selector: str) -> str:
        """Return the current value of an <input> element."""
        return self.page.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        """Return True if the element is currently visible on the page."""
        return self.page.locator(selector).is_visible()

    def wait_for_visible(self, selector: str, timeout: int = Timeouts.DEFAULT) -> None:
        """Block until the element becomes visible (or timeout raises)."""
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)

    def expect_to_be_visible(self, selector: str, timeout: int = Timeouts.DEFAULT) -> None:
        """Assert that the element is visible within the timeout period."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
        

    def wait_for_url_contains(self, partial: str, timeout: int = Timeouts.NAVIGATION) -> None:
        """
        Block until the current URL contains the given string.

        Uses Playwright's built-in retry — more reliable than a plain assert
        because it handles slow redirects and async navigation automatically.
        """
        self.page.wait_for_url(f"**{partial}**", timeout=timeout)

    def wait_time(self, milliseconds: int) -> None:
        """Pause execution for a fixed amount of time (in milliseconds)."""
        self.page.wait_for_timeout(milliseconds)