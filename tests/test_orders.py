import pytest
import allure
from utils.api_client import ApiClient

@allure.title("Заказы: неавторизованный пользователь не может создать заказ")
@allure.description("Проверяем, что при отсутствии токена в заголовке Authorization сервер возвращает ошибку 401/403.")
@allure.severity(allure.severity_level.CRITICAL)
def test_order_creation_requires_auth(client, ingredients):
    
    
    # пытаемся создать заказ БЕЗ токена
    resp = client.create_order(ingredients, access_token=None)
    
    
    assert resp.status_code in (401, 403), f"Ожидался 401/403, получен {resp.status_code}"

@allure.title("Заказы: авторизованный пользователь успешно создает заказ")
@allure.description("Проверяем, что при наличии валидного токена в заголовке Authorization заказ создается (200 OK).")
@allure.severity(allure.severity_level.CRITICAL)
def test_order_creation_success(client, ingredients, registered_user):
    # берем токен из зарегистрированного пользователя
    access_token = registered_user["access_token"]
    
    # создаем заказ С токеном
    resp = client.create_order(ingredients, access_token=access_token)
    
    # проверяем успех и структуру ответа
    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}, body={resp.text}"
    
    order_data = resp.json()
    assert order_data.get("success") is True
    assert "order" in order_data
    assert "number" in order_data["order"]


@allure.title("Заказы: ошибка при создании заказа без ингредиентов")
@allure.description("Проверяем, что сервер возвращает 400 и сообщение об ошибке, если не передан ни один ингредиент.")
@allure.severity(allure.severity_level.CRITICAL)
def test_order_without_ingredients(client, registered_user):
    access_token = registered_user["access_token"]
    
    # передаем пустой список
    resp = client.create_order(ingredients= {}, access_token=access_token)
    
    # Статус 400
    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"
    
    # Структура ответа (как в документации)
    data = resp.json()
    assert data.get("success") is False
    assert data.get("message") == "Ingredient ids must be provided"

@allure.title("Заказы: ошибка сервера при передаче неверного ID ингредиента")
@allure.description("Проверяем, что сервер возвращает 500 Internal Server Error при передаче невалидного хеша ингредиента.")
@allure.severity(allure.severity_level.NORMAL)
def test_order_with_invalid_ingredient_id(client, registered_user):
    access_token = registered_user["access_token"]
    
    #  передаём явно несуществующий ID 
    resp = client.create_order(ingredients=["INVALID_ID_12345678901234567890"], access_token=access_token)
    
    #  Статус 500
    assert resp.status_code == 500, f"Ожидался 500, получен {resp.status_code}"
    
@allure.title("Заказы: создание заказа с корректным списком ингредиентов")
@allure.description(
    "Проверяем, что авторизованный пользователь может создать заказ, передав валидный список ID ингредиентов. "
    "Согласно документации API, при корректных данных сервер должен вернуть статус 200 и номер заказа."
)
@allure.severity(allure.severity_level.CRITICAL)
def test_order_creation_with_ingredients(client, ingredients, registered_user):
    # берем чистый токен и список ID ингредиентов
    access_token = registered_user["access_token"]
    
    # отправляем запрос на создание заказа
    resp = client.create_order(ingredients=ingredients, access_token=access_token)
    
    #  проверяем статус код 200 (успех)
    assert resp.status_code == 200, f"Ожидался статус 200, получен {resp.status_code}"
    
    # парсим JSON и проверяем структуру ответа
    data = resp.json()
    
    # Проверяем флаг успеха
    assert data.get("success") is True, "Флаг 'success' должен быть True"
    
    # Проверяем наличие объекта заказа и его номера
    assert "order" in data, "В ответе должен присутствовать объект 'order'"
    assert "number" in data["order"], "В объекте 'order' должен быть ключ 'number' (номер заказа)"
    
    # Проверяем, что в заказе действительно сохранились переданные ингредиенты
    # (это дополнительная страховка, что мы передали именно то, что хотели)
    assert "ingredients" in data["order"]
    assert isinstance(data["order"]["ingredients"], list)
    assert len(data["order"]["ingredients"]) == len(ingredients), "Количество ингредиентов в ответе должно совпадать с отправленным"
