import pytest
import requests
import uuid

@pytest.fixture(scope="function")
def base_url():
    return "https://stellarburgers.education-services.ru"

@pytest.fixture(scope="function")
def registered_user(base_url):
    """
    Создаёт тестового пользователя. Если он уже есть — использует его.
    Возвращает dict с email и password.
    """
    # Генерируем уникальный email, чтобы не было конфликтов между запусками
    unique_email = f"test_auto_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "password": "12345",
        "name": "Auto User"
    }

    register_url = f"{base_url}/api/users/"
    resp = requests.post(register_url, json=payload)

    if resp.status_code == 200:
        # Пользователь успешно создан
        return payload
    elif resp.status_code == 409:
        # Пользователь уже существует (редкий случай при UUID, но бывает)
        # Просто вернём те же данные — он уже есть, можно логиниться
        return payload
    else:
        raise RuntimeError(
            f"Не удалось подготовить тестового пользователя: "
            f"статус {resp.status_code}, ответ: {resp.text}"
        )
