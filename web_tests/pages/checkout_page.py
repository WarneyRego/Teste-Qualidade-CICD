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
        self.wait = WebDriverWait(driver, 15)

    def _set_input(self, locator, value: str):
        """Set input value firing React-compatible events so form validation passes."""
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("""
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            setter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
            arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
        """, el, value)

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        self.wait.until(EC.url_contains("checkout-step-one"))
        self._set_input(self._FIRST_NAME, first_name)
        self._set_input(self._LAST_NAME, last_name)
        self._set_input(self._POSTAL_CODE, postal_code)
        self.wait.until(EC.element_to_be_clickable(self._CONTINUE_BTN)).click()
        self.wait.until(EC.url_contains("checkout-step-two"))

    def get_item_total_label(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self._ITEM_TOTAL_LABEL)).text

    def finish_order(self):
        self.wait.until(EC.element_to_be_clickable(self._FINISH_BTN)).click()
        self.wait.until(EC.presence_of_element_located(self._CONFIRMATION_HEADER))

    def get_confirmation_header(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_HEADER).text

    def get_confirmation_text(self) -> str:
        return self.driver.find_element(*self._CONFIRMATION_TEXT).text
