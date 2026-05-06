from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CheckoutPage:
    # Step 1 — customer info
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")

    # Step 2 — order overview
    _ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    _FINISH_BTN = (By.ID, "finish")

    # Step 3 — confirmation
    _CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    _CONFIRMATION_TEXT = (By.CLASS_NAME, "complete-text")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.driver.find_element(*self._FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self._LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self._POSTAL_CODE).send_keys(postal_code)
        self.driver.find_element(*self._CONTINUE_BTN).click()

    def get_item_total_label(self) -> str:
        return self.driver.find_element(*self._ITEM_TOTAL_LABEL).text

    def finish_order(self):
        self.driver.find_element(*self._FINISH_BTN).click()

    def get_confirmation_header(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_HEADER).text

    def get_confirmation_text(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_TEXT).text
