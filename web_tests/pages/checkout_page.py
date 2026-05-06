from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    _FIRST_NAME  = (By.ID, "first-name")
    _LAST_NAME   = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    _FINISH_BTN  = (By.ID, "finish")
    _CONFIRMATION_HEADER = (By.CLASS_NAME, "complete-header")
    _CONFIRMATION_TEXT   = (By.CLASS_NAME, "complete-text")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.wait.until(EC.presence_of_element_located(self._FIRST_NAME)).send_keys(first_name)
        self.driver.find_element(*self._LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self._POSTAL_CODE).send_keys(postal_code)
        btn = self.driver.find_element(*self._CONTINUE_BTN)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.url_contains("checkout-step-two"))

    def get_item_total_label(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self._ITEM_TOTAL_LABEL)).text

    def finish_order(self):
        btn = self.wait.until(EC.presence_of_element_located(self._FINISH_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(EC.presence_of_element_located(self._CONFIRMATION_HEADER))

    def get_confirmation_header(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_HEADER).text

    def get_confirmation_text(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_TEXT).text
