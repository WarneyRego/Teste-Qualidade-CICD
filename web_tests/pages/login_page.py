from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    URL = "https://www.saucedemo.com/"

    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username: str, password: str):
        self.driver.find_element(*self._USERNAME).clear()
        self.driver.find_element(*self._USERNAME).send_keys(username)
        self.driver.find_element(*self._PASSWORD).clear()
        self.driver.find_element(*self._PASSWORD).send_keys(password)
        self.driver.find_element(*self._LOGIN_BTN).click()

    def get_error_message(self) -> str:
        return self.driver.find_element(*self._ERROR_MSG).text
