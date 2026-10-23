import pytest
import allure
import requests

LOGIN_PATH = "/api/auth/login"

@allure.title("Авторизация: вход под существующим пользователем")
@allure.description(
    "Сценарий: регистрация тестового пользователя → успешная авторизация. "
    "Проверяем статус 200, success=true, наличие accessToken и совпадение email."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_login_existing_user(base_url, registered_user):
    url = base_url + LOGIN_PATH
    payload = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }

    resp = requests.post(url, json=payload)

    assert resp.status_code == 200, f"Ожидался статус 200, получен {resp.status_code}"
    data = resp.json()

    assert data.get("success") is True, "Поле success должно быть True"
    assert "accessToken" in data, "В ответе должен присутствовать accessToken"
    assert (
        "user" in data and data["user"]["email"] == payload["email"]
    ), "Email в ответе не совпадает с отправленным"


@allure.title("Авторизация: ошибка при неверных логине и пароле")
@allure.description(
    "Сценарий: попытка входа с заведомо неверными данными. "
    "Проверяем статус 401, success=false и корректное сообщение об ошибке."
)
@allure.severity(allure.severity_level.NORMAL)
def test_login_invalid_credentials(base_url):
    url = base_url + LOGIN_PATH
    # Специально неверные данные
    payload = {"email": "bad@example.com", "password": "wrong"}

    resp = requests.post(url, json=payload)

    assert resp.status_code == 401, f"Ожидался статус 401, получен {resp.status_code}"
    data = resp.json()

    assert data.get("success") is False, "Поле success должно быть False"
    expected_message = "email or password are incorrect"
    assert (
        data.get("message") == expected_message
    ), f"Сообщение об ошибке не совпадает: ожидалось '{expected_message}', получено '{data.get('message')}'"
