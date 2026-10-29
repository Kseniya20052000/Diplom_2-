import pytest
import allure
import uuid
from utils.api_client import ApiClient

@allure.title("Регистрация: успешный сценарий с заполнением всех обязательных полей")
@allure.description("Проверяем, что пользователь успешно регистрируется при передаче email, password и name. Ожидается статус 200.")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_unique_user(base_url):
    client = ApiClient(base_url)
    # Генерируем уникальный email, чтобы не было конфликта
    unique_email = f"test_auto_{uuid.uuid4().hex[:8]}@example.com"
    
    resp = client.register_user(
        email=unique_email, 
        password="12345", 
        name="Auto User"  # Поле name обязательно согласно документации
    )
    
    assert resp.status_code == 200, f"Ожидался статус 200, получен {resp.status_code}, body={resp.text}"
    data = resp.json()
    assert data.get("success") is True

@allure.title("Регистрация: попытка повторной регистрации существующего пользователя")
@allure.description("Проверяем реакцию API, если пользователь уже есть в базе. Согласно документации: статус 403, сообщение 'User already exists'.")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_existing_user(base_url):
    client = ApiClient(base_url)
    unique_email = f"test_dup_{uuid.uuid4().hex[:8]}@example.com"
    
    # 1. Сначала регистрируем пользователя
    resp_create = client.register_user(email=unique_email, password="12345", name="Dup User")
    assert resp_create.status_code == 200, "Не удалось создать тестового пользователя для проверки дублей"
    
    # 2. Пытаемся зарегистрировать того же самого
    resp_duplicate = client.register_user(email=unique_email, password="12345", name="Dup User")
    
    
    assert resp_duplicate.status_code == 403, f"Ожидался статус 403, получен {resp_duplicate.status_code}"
    
    data = resp_duplicate.json()
    assert data.get("success") is False
    assert data.get("message") == "User already exists"

@allure.title("Регистрация: отсутствие обязательных полей")
@allure.description("Проверяем валидацию обязательных полей (email, password, name). Согласно документации: статус 403, сообщение о требуемых полях.")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_user_missing_fields(client):
    
    unique_email = f"test_miss_{uuid.uuid4().hex[:8]}@example.com"
    
    # Пытаемся зарегистрироваться БЕЗ поля name 
    # Документация говорит, что все три поля обязательны
    resp = client.register_user(email=unique_email, password="12345", name=None)
    
    
    assert resp.status_code == 403, f"Ожидался статус 403, получен {resp.status_code}"
    
    data = resp.json()
    assert data.get("success") is False
    
    assert data.get("message") == "Email, password and name are required fields"
