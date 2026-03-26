# # tests/test_user_must_sign_in_on_cart_payment_flow.py
# import pytest
# from pages.home_page import HomePage


# class TestUserMustSignInOnCartPaymentFlow:

#     @pytest.mark.smoke
#     @pytest.mark.shufersal
#     def test_search_results_contain_item_user_typed_in_search_bar(self, home_page):
        
#         item_that_user_search = "חלב"
#         item_added_to_cart = ""
#         item_in_cart = ""

#         # Step 1 + 2 + 3: open site, type keyword, wait for dropdown
#         home_page.open()
#         home_page.type_user_requested_item_to_search_bar(item_that_user_search)
        
#         # home_page.expect_to_be_visible(home_page.ITEMS_SEARCH_RESULT_LIST).first
#         home_page.wait_time(1000)
        
#         # Step 4: get all suggestion texts
#         items = home_page.get_search_result_items_list()
#         print("assert we got 10 results for the search")
#         assert len(items) == 10, f"Expected 10 search suggestions but got {len(items)}"

#         # Print all items to console for debugging (visible with pytest -s)
#         print(f"\nFound {len(items)} suggestions:")
#         for i, text in enumerate(items, start=1):
#             print(f"  {i}. {text}")

#         item_added_to_cart =items[0]

#         # Step 5: verify every item contains the string that the user typed
#         print("verify every item in the results contains the string user submitted")
#         failing = [text for text in items if item_that_user_search not in text]
#         assert len(failing) == 0, (
#             f"These suggestions do not contain '{item_that_user_search}':\n"
#             + "\n".join(f"  - {t}" for t in failing)
#         )

#         # Step 6: click the first 'Add to cart' button in the dropdown
#         home_page.click_add_to_cart_of_first_item()

#         # Step 7: verify the item name in the cart contains the search keyword
#         cart_item_name = home_page.get_cart_item_name()
#         assert item_that_user_search in cart_item_name, (
#             f"Expected cart item name to contain '{item_that_user_search}' but got '{cart_item_name}'"
#         )
#         # Step 8: verify the name in the cart is the name actually added
#         home_page.print_cart_item_name()    
#         item_in_cart = home_page.get_cart_item_name()
#         print(f"Comparing- item_added: '{item_added_to_cart}', item_in_cart: '{item_in_cart}'")
#         assert item_added_to_cart == item_in_cart, (f"Item added: '{item_added_to_cart}' does not match item in cart: '{item_in_cart}'")
        
#         # Step 8.1: test quantity of item in cart:
#         quantity = home_page.get_first_item_in_cart_quantity()
#         print(f"Quantity of the first item in the cart: {quantity}")
#         assert quantity == 1, f"Expected quantity to be 1 but got {quantity}"

#         # Step 9: click the 'For payment' button in the cart
#         home_page.click_on_for_payment_button()

#         # Step 10: verify that the user is redirected to the login page
#         print("verify that the user is redirected to the login page")
#         assert home_page.is_login_page_visible(), ("User was not directed to login page as expected")

