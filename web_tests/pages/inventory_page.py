from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    _TITLE = (By.CLASS_NAME, "title")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_page_title(self) -> str:
        return self.driver.find_element(*self._TITLE).text

    def add_item_to_cart(self, item_name: str):
        # The add-to-cart button id is derived from the lowercased, hyphenated item name
        normalized = item_name.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")
        btn_id = f"add-to-cart-{normalized}"
        self.driver.find_element(By.ID, btn_id).click()

    def get_cart_item_count(self) -> int:
        elements = self.driver.find_elements(*self._CART_BADGE)
        if not elements:
            return 0
        return int(elements[0].text)

    def go_to_cart(self):
        self.driver.find_element(*self._CART_LINK).click()
