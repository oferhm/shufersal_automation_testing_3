# pages/home_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.constants import URLs


class HomePage(BasePage):

    # ── Selectors ─────────────────────────────────────────────────────────────
    _SEARCH_INPUT   = "#js-site-search-input"
    _RETURNED_ITEMS = ".tt-menu .tile .text"

    # ── Search term ───────────────────────────────────────────────────────────
    USER_SEARCH_INPUT = "חלב"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "HomePage":
        """Navigate to the Shufersal home page."""
        self.navigate(URLs.HOME)
        return self

    def type_search_keyword(self, keyword: str) -> "HomePage":
        """
        Type a keyword into the search input.
        No Enter needed — the dropdown appears automatically after typing.
        We wait 2 seconds for the autocomplete results to load.
        """
        self.fill(self._SEARCH_INPUT, keyword)
        self.page.wait_for_timeout(2000)  # wait for dropdown to populate
        return self

    def get_search_suggestion_items(self) -> list[str]:
        """
        Return the inner text of every suggestion item in the dropdown.
        Selector: .tt-menu .tile .text  (expected: ~20 items)
        """
        locators = self.page.locator(self._RETURNED_ITEMS).all()
        return [item.inner_text() for item in locators]