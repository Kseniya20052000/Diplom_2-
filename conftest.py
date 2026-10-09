import pytest

@pytest.fixture(scope="session")
def base_url():
    return "https://stellarburgers.education-services.ru"