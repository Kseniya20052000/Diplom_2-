import pytest
import requests
import uuid
from utils.api_client import ApiClient

@pytest.fixture(scope="function")
def base_url():
    return "https://stellarburgers.education-services.ru"

@pytest.fixture(scope="function")
def client(base_url):
    """Возвращает готовый клиент для работы с API."""
    return ApiClient(base_url)

@pytest.fixture(scope="function")
def ingredients(client):
    """Получает список ингредиентов. Если не удается - тест пропускается."""
    try:
        ingrs = client.get_ingredients()
        if len(ingrs) < 2:
            pytest.skip("Недостаточно ингредиентов на стенде для теста")
        return ingrs
    except Exception:
        pytest.skip("Не удалось получить ингредиенты. Стенд недоступен.")

@pytest.fixture(scope="function")
def registered_user(client):
    """Регистрирует нового пользователя и возвращает его токены."""
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    resp = client.register_user(email=unique_email, password="12345", name="Test User")
    
    if resp.status_code != 200:
        pytest.skip(f"Не удалось зарегистрировать тестового пользователя. Статус: {resp.status_code}")
    
    data = resp.json()
    raw_token = data.get("accessToken")
    
    
    if raw_token and raw_token.startswith("Bearer "):
        clean_token = raw_token.replace("Bearer ", "", 1)
    else:
        clean_token = raw_token
        
    return {
        "email": unique_email,
        "access_token": clean_token,  
        "refresh_token": data.get("refreshToken")
    }