import pytest
import allure
from utils.api_client import ApiClient
import uuid

@allure.title("Авторизация: вход под существующим пользователем")
@allure.description("Проверяем, что пользователь может успешно войти в систему.")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_existing_user(base_url):
    client = ApiClient(base_url)
    
    #  Сначала регистрируем пользователя, чтобы он точно существовал
    unique_email = f"login_test_{uuid.uuid4().hex[:8]}@example.com"
    reg_resp = client.register_user(email=unique_email, password="12345", name="Login User")
    
    if reg_resp.status_code != 200:
        pytest.skip("Не удалось зарегистрировать пользователя для теста логина")

    # Пытаемся войти
    resp = client.login_user(email=unique_email, password="12345")
    
    # Проверяем успех
    assert resp.status_code == 200
    data = resp.json()
    assert "accessToken" in data
    assert "refreshToken" in data
    assert data["success"] is True

@allure.title("Авторизация: вход с неверными учётными данными")
@allure.description("Проверяем, что вход с неправильным паролем отклоняется.")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_wrong_credentials(client):
    email = f"wrong_cred_{uuid.uuid4().hex[:8]}@example.com"
    # Сначала зарегистрируем, чтобы пользователь точно существовал
    reg_resp = client.register_user(email=email, password="12345", name="Test User")
    assert reg_resp.status_code == 200

    # Пытаемся войти с неправильным паролем
    resp = client.login_user(email=email, password="wrong_password_123")

    assert resp.status_code in (401, 403) or (resp.status_code == 200 and resp.json().get("success") is False)
