# pages/home_page.py
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.constants import URLs


class HomePage(BasePage):

    # ── Selectors ─────────────────────────────────────────────────────────────
    SEARCH_BAR            = "#js-site-search-input"
    ITEMS_SEARCH_RESULT_LIST     = ".tt-menu .tile button.text"
    # ADD_TO_CART_BUTTON_LIST = ".tt-menu .tile .addToCart .js-add-to-cart"
    ADD_TO_CART_BUTTON_LIST = ".tt-menu .tile .addToCart .btn.js-add-to-cart"
    ADD_TO_CART_BUTTON_OF_FIRST_ITEM = ".tt-menu .tile:first-of-type .addToCart .js-add-to-cart"
    ITEMS_NAME_IN_CART_LIST       = ".miglog-prod-body .miglog-text3"
    SHOW_CART_ARROW_BUTTON = "button[data-target=\"#main\"]"
    POP_UP_EVIDENCE = ".tabsDetails"
    POP_UP_WINDOW_CLOSE_BUTTON = ".text-header .btnClose"
    ITEMS_SECTION_LIST = ".tt-dataset .tile"
    FIRST_SECTION_OF_FIRST_ITEM = ".tt-dataset .tile:first-of-type"
    FIRST_SECTION_OF_FIRST_ITEM_1 = ".tt-dataset .tile[data-index=\"0\"]"
    FOR_PAYMENT_BUTTON = ".wrapper-btnSubmit .title-btn"
    LOGIN_PAGE_EVIDENCE = "#j_username"
    CART_ITEM_QUANTITY_INPUT = ".miglog-prod-qtForm-wrapper .spinContainer"  # selector is hidden, should hover element
    CART_ITEM_FOR_HOVER = ".wrapper-miglog-prod-body"  # selector for hovering to reveal quantity input

    


       
    items_full_name_result_list = ""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "HomePage":
        """Navigate to the Shufersal home page."""
        self.navigate(URLs.HOME)
        return self

    def type_user_requested_item_to_search_bar(self, item_to_search: str) -> "HomePage":
        """
        Type a string of item requested into the search input
        No Enter needed — dropdown appears automatically.
        """
        self.fill(self.SEARCH_BAR, item_to_search)
        self.page.locator(self.ITEMS_SEARCH_RESULT_LIST).first.wait_for(state="visible")
        return self

    def get_search_result_items_list(self) -> list[str]:
        """
        Return the full name of every suggestion item in the dropdown after search request.
        (expected: 10 items)
        """
        print("\n--- get_search_result_items_list ---")
        locators = self.page.locator(self.ITEMS_SEARCH_RESULT_LIST).all()
        return [locator.inner_text() for locator in locators]
    

    def return_add_to_cart_buttons_as_list(self) -> list:
        """
        Return a list of all 'Add to cart' button locators from the dropdown.
        Selector: .tt-menu .tile .addToCart .js-add-to-cart
        """
        return self.page.locator(self.ADD_TO_CART_BUTTON_LIST).all()

    def click_add_to_cart_of_first_item(self) -> "HomePage":
        """
        Click the first 'Add to cart' button in the dropdown suggestion list.
        Waits for the button to be visible before clicking.
        """
        self.remove_order_pop_up_window_if_pops()

        
        items = self.page.locator(self.ITEMS_SECTION_LIST)

        items.first.wait_for(state="visible")
        items.first.hover()
        
        # Wait for the first button to be visible, then click it
        self.click_first_element(self.ADD_TO_CART_BUTTON_LIST)

        self.remove_order_pop_up_window_if_pops()

        return self
    
    def click_on_show_cart_arrow_button(self) -> "HomePage":
        """
        Click the arrow button that opens the cart panel after adding an item.
        Selector: button[data-target="#main"]
        """
        self.remove_order_pop_up_window_if_pops()

        # Use the BasePage click method instead of manual locator handling
        self.page.locator(self.SHOW_CART_ARROW_BUTTON).wait_for(state="visible")
        self.click(self.SHOW_CART_ARROW_BUTTON)
        return self

    def get_cart_item_name(self) -> str:
        """
        Return the name of the item shown in the cart panel after adding.
        """

        # Use the BasePage get_text method which handles waiting properly
        self.remove_order_pop_up_window_if_pops()

        self.wait_time(1000) # Wait for the cart item name to be visible (adjust as needed)
        self.remove_order_pop_up_window_if_pops()

        return self.get_text_of_first_element(self.ITEMS_NAME_IN_CART_LIST)

    def print_cart_item_name(self) -> None:
        """Print the cart item name to console."""
        self.wait_time(1000)
        name = self.get_cart_item_name()
        print(f"\nItem added to cart: {name}")


    def remove_order_pop_up_window_if_pops(self) -> "HomePage":
        """
        Check if a pop-up window appears after adding an item to the cart.
        If it appears, close it by clicking the 'X' button.
        """
        # Check if popup is visible and close it if needed
        if self.is_visible(self.POP_UP_EVIDENCE):
            print("Pop-up window appeared. Closing it.")
            self.click(self.POP_UP_WINDOW_CLOSE_BUTTON)
        
        return self
    
    def click_on_for_payment_button(self) -> "HomePage":
        """
        Click the 'For payment' button in the cart panel to proceed to checkout.
        Selector: .wrapper-btnSubmit
        """
        # Wait for the button to be visible, then click it
        self.wait_time(1000) # Wait for the button to be visible (adjust as needed)
        self.click(self.FOR_PAYMENT_BUTTON)

        return self
    
    def is_login_page_visible(self) -> bool:
        """
        Check if the current page is the login page by looking for a unique element.
        Selector: #j_username (the username input field)
        """
        self.wait_time(1000) # Wait for the login page to load (adjust as needed)
        return self.is_visible(self.LOGIN_PAGE_EVIDENCE)
    
    def get_first_item_in_cart_quantity(self) -> int:
        """
        Return the quantity of the first item in the cart.
        Selector for quantity input: .miglog-prod-body .quantity input
        """
        
        self.hover(self.CART_ITEM_FOR_HOVER)    
        self.wait_time(3000)
        quantity_str = self.get_input_value(self.CART_ITEM_QUANTITY_INPUT)
        print(f"Quantity string from input: '{quantity_str}'")
        return int(quantity_str) if quantity_str.isdigit() else 0