import pytest
import random
from utils.api_client import ApiClient

@pytest.fixture(scope="session")
def base_url():
    return "https://stellarburgers.education-services.ru"

@pytest.fixture
def api_client(base_url):
    return ApiClient(base_url)

@pytest.fixture
def unique_user_data():
    random_id = random.randint(100000, 999999)
    return {
        "email": f"test_user_{random_id}@example.com",
        "password": "TestPass123",
        "name": f"Test User {random_id}"
    }

@pytest.fixture(scope="function")
def existing_user(api_client, unique_user_data):
    """
    Фикстура создаёт пользователя перед тестом и возвращает его данные.
    Гарантирует, что пользователь точно существует.
    """
    response = api_client.register_user(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=unique_user_data["name"]
    )
    
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать тестового пользователя для фикстуры existing_user. Статус: {response.status_code}, ответ: {response.text}")
