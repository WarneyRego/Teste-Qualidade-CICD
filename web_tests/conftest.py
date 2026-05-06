import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # headless=True in CI; remove this arg to watch the browser locally
    if os.getenv("CI"):
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    # disable Chrome password manager popups that can block test interactions
    options.add_argument("--disable-features=PasswordCheck,SafeBrowsingEnhancedProtection")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    })

    service = Service(ChromeDriverManager().install())
    chrome = webdriver.Chrome(service=service, options=options)

    yield chrome

    chrome.quit()
