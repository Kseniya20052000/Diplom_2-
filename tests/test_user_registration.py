import pytest
import allure  
from utils.api_client import ApiClient

@allure.title("Регистрация нового пользователя: успешный сценарий")
@allure.description("Проверяем, что API позволяет зарегистрировать уникального пользователя и возвращает статус 200")
def test_create_unique_user(api_client, unique_user_data):
    """Сценарий 1: создать уникального пользователя"""
    response = api_client.register_user(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=unique_user_data["name"]
    )
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
    assert response.json().get("success") is True, "Поле success должно быть True"


@allure.title("Попытка повторной регистрации: пользователь уже существует")
@allure.description("Проверяем, что API отклоняет регистрацию существующего пользователя и возвращает корректный код ошибки")
def test_create_existing_user(api_client, existing_user):
    """Сценарий 2: попытка зарегистрировать уже существующего пользователя"""
    
    response = api_client.register_user(
        email=existing_user["email"],
        password=existing_user["password"],
        name=existing_user["name"]
    )
    
    assert response.status_code in (400, 403, 409), f"Ожидался код ошибки (400/403/409), получен {response.status_code}"
    
    message = response.json().get("message", "")
    assert "already exists" in str(message).lower(), f"Сообщение об ошибке не совпадает: {message}"


@allure.title("Регистрация без обязательного поля name: проверка валидации")
@allure.description("Проверяем, что API отклоняет запрос, если не передано обязательное поле name")
def test_create_user_missing_field(api_client, unique_user_data):
    """Сценарий 3: не передать обязательное поле name"""
    response = api_client.register_user(
        email=unique_user_data["email"],
        password=unique_user_data["password"],
        name=None  
    )
    
    assert response.status_code in (400, 403), f"Ожидался код ошибки, получен {response.status_code}"
    
    message = response.json().get("message", "")
    assert "required" in str(message).lower(), f"Сообщение не содержит указания на обязательные поля: {message}"
