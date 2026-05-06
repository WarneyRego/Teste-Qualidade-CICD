import pytest
import requests
from datetime import datetime

from api_tests.services.pet_service import PetService
from api_tests.services.store_service import StoreService
from api_tests.services.user_service import UserService

BASE_URL = "https://petstore.swagger.io/v2"


def pytest_html_report_title(report):
    report.title = "API Tests — Petstore"


def pytest_configure(config):
    config._metadata = {
        "Projeto": "Automação de Testes — Qualidade & CI/CD",
        "Suite": "API Tests · Swagger Petstore",
        "Base URL": BASE_URL,
        "Gerado em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json", "Accept": "application/json"})
    yield s
    s.close()


@pytest.fixture(scope="session")
def pet_service(session):
    return PetService(BASE_URL, session)


@pytest.fixture(scope="session")
def store_service(session):
    return StoreService(BASE_URL, session)


@pytest.fixture(scope="session")
def user_service(session):
    return UserService(BASE_URL, session)
