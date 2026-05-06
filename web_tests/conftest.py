import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    if os.getenv("CI"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    # Selenium 4.6+ selenium-manager auto-resolves chromedriver
    chrome = webdriver.Chrome(options=options)

    yield chrome

    chrome.quit()
