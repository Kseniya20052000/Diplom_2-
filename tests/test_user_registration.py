import pytest
from utils.api_client import ApiClient

@pytest.fixture
def api_client(base_url):
    return ApiClient(base_url)

@pytest.fixture
def unique_user_data():
    # Генерируем уникальные данные для каждого запуска
    import random
    random_id = random.randint(100000, 999999)
    return {
        "email": f"test_user_{random_id}@example.com",
        "password": "TestPass123",
        "name": f"Test User {random_id}"
    }

@pytest.fixture
def existing_user_data():
    # Данные существующего пользователя (заранее зарегистрированного)
    return {
        "email": "test-data@yandex.ru",
        "password": "password",
        "name": "Username"
    }

def test_create_unique_user(api_client, unique_user_data):
    """Сценарий 1: создать уникального пользователя"""
    response = api_client.register_user(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=unique_user_data["name"]
    )
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert response.json().get("success") is True, "Поле success должно быть True"

def test_create_existing_user(api_client, existing_user_data):
    """Сценарий 2: создать пользователя, который уже зарегистрирован"""
    response = api_client.register_user(
        email=existing_user_data["email"],
        password=existing_user_data["password"],
        name=existing_user_data["name"]
    )
    assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
    assert response.json().get("message") == "User already exists", "Сообщение об ошибке не совпадает"

def test_create_user_missing_field(api_client, unique_user_data):
    """Сценарий 3: создать пользователя и не заполнить одно из обязательных полей"""
    # Пропустим поле name
    response = api_client.register_user(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=None  # или вообще не передавать ключ name
    )
    assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
    assert "required" in response.json().get("message", "").lower(), "Сообщение должно содержать указание на обязательные поля"
