# tests/test_user_must_sign_in_on_cart_payment_flow.py
import pytest
from pages.home_page import HomePage

SEARCH_KEYWORD = "חלב"


class TestUserMustSignInOnCartPaymentFlow:

    @pytest.fixture(autouse=False)
    def searched_items(self, home_page):
        """Open site and type keyword — reused by tests that need the dropdown."""
        home_page.open()
        home_page.type_user_requested_item_to_search_bar(SEARCH_KEYWORD)
        home_page.wait_time(1000)
        return home_page.get_search_result_items_list()

    @pytest.fixture(autouse=False)
    def item_added_to_cart(self, home_page, searched_items):
        """Add the first item to cart and return its name."""
        first_item_name = searched_items[0]
        home_page.click_add_to_cart_of_first_item()
        return first_item_name

    # ── Tests ─────────────────────────────────────────────────────────────────

    @pytest.mark.smoke
    def test_search_returns_10_suggestions(self, searched_items):
        """Dropdown must contain exactly 10 suggestions."""
        assert len(searched_items) == 10, (
            f"Expected 10 search suggestions but got {len(searched_items)}"
        )

    @pytest.mark.smoke
    def test_all_suggestions_contain_search_keyword(self, searched_items):
        """Every suggestion in the dropdown must contain the search keyword."""
        failing = [text for text in searched_items if SEARCH_KEYWORD not in text]
        assert len(failing) == 0, (
            f"These suggestions do not contain '{SEARCH_KEYWORD}':\n"
            + "\n".join(f"  - {t}" for t in failing)
        )

    @pytest.mark.smoke
    def test_cart_item_contains_search_keyword(self, home_page, item_added_to_cart):
        """Item name shown in cart must contain the search keyword."""
        cart_item_name = home_page.get_cart_item_name()
        assert SEARCH_KEYWORD in cart_item_name, (
            f"Expected cart item to contain '{SEARCH_KEYWORD}' but got '{cart_item_name}'"
        )

    @pytest.mark.smoke
    def test_cart_shows_correct_item_name(self, home_page, item_added_to_cart):
        """Item name in cart must match the name of the item that was added."""
        item_in_cart = home_page.get_cart_item_name()
        assert item_added_to_cart == item_in_cart, (
            f"Item added: '{item_added_to_cart}' does not match item in cart: '{item_in_cart}'"
        )

    @pytest.mark.smoke
    def test_cart_item_default_quantity_is_one(self, home_page, item_added_to_cart):
        """Newly added item must have a default quantity of 1."""
        quantity = home_page.get_first_item_in_cart_quantity()
        assert quantity == 1, f"Expected quantity 1 but got {quantity}"

    @pytest.mark.smoke
    def test_payment_flow_redirects_to_login(self, home_page, item_added_to_cart):
        """Clicking 'For payment' must redirect an unauthenticated user to the login page."""
        home_page.click_on_for_payment_button()
        assert home_page.is_login_page_visible(), (
            "User was not redirected to the login page as expected"
        )