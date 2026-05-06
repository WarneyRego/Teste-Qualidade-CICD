import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_html_report_title(report):
    report.title = "Web Tests — SauceDemo"


def pytest_configure(config):
    config._metadata = {
        "Projeto": "Automação de Testes — Qualidade & CI/CD",
        "Suite": "Web E2E Tests · SauceDemo",
        "URL": "https://www.saucedemo.com",
        "Ferramenta": "Selenium + Page Object Model",
        "Gerado em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


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

    service = Service(ChromeDriverManager().install())
    chrome = webdriver.Chrome(service=service, options=options)
    chrome.implicitly_wait(10)

    yield chrome

    chrome.quit()
