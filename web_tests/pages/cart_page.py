from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    _CART_ITEMS  = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES  = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_item_names(self) -> list:
        self.wait.until(EC.presence_of_element_located(self._CART_ITEMS))
        return [el.text for el in self.driver.find_elements(*self._ITEM_NAMES)]

    def get_item_count(self) -> int:
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def proceed_to_checkout(self):
        btn = self.wait.until(EC.presence_of_element_located(self._CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.url_contains("checkout-step-one"))
