import pytest

from web_tests.pages.login_page import LoginPage
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.cart_page import CartPage
from web_tests.pages.checkout_page import CheckoutPage

USERNAME = "standard_user"
PASSWORD = "secret_sauce"

ITEMS_TO_BUY = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
]


def test_complete_purchase_flow(driver):
    # --- Login ---
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(USERNAME, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.get_page_title() == "Products"

    # --- Add two items to the cart ---
    for item in ITEMS_TO_BUY:
        inventory_page.add_item_to_cart(item)

    assert inventory_page.get_cart_item_count() == len(ITEMS_TO_BUY)

    # --- Navigate to cart and verify contents ---
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_item_count() == len(ITEMS_TO_BUY)

    cart_item_names = cart_page.get_item_names()
    for item in ITEMS_TO_BUY:
        assert item in cart_item_names

    # --- Proceed to checkout ---
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_customer_info("John", "Doe", "12345")

    # Verify the order summary shows a subtotal before finishing
    item_total = checkout_page.get_item_total_label()
    assert "Item total:" in item_total

    # --- Complete the purchase ---
    checkout_page.finish_order()

    assert checkout_page.get_confirmation_header() == "Thank you for your order!"
    assert "dispatched" in checkout_page.get_confirmation_text().lower()
