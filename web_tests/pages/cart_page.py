from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CartPage:
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")
    _CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self._ITEM_NAMES)]

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def proceed_to_checkout(self):
        self.driver.find_element(*self._CHECKOUT_BTN).click()
