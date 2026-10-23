import pytest
import allure
import requests

BASE_PATH = "/api/orders"

@allure.title("Создание заказа: с авторизацией и валидными ингредиентами")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order_authorized(base_url, auth_header):
    url = base_url + BASE_PATH
    payload = {"ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]}
    resp = requests.post(url, json=payload, headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("success") is True
    assert "order" in data and "number" in data["order"]

@allure.title("Создание заказа: без авторизации, но с ингредиентами")
@allure.severity(allure.severity_level.NORMAL)
def test_create_order_unauthorized(base_url):
    url = base_url + BASE_PATH
    payload = {"ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]}
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("success") is True

@allure.title("Создание заказа: без ингредиентов")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order_no_ingredients(base_url, auth_header):
    url = base_url + BASE_PATH
    payload = {"ingredients": [ ]}
    resp = requests.post(url, json=payload, headers=auth_header)
    assert resp.status_code == 400
    data = resp.json()
    assert data.get("success") is False
    assert data.get("message") == "Ingredient ids must be provided"

@allure.title("Создание заказа: с неверным хешем ингредиента")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order_invalid_hash(base_url, auth_header):
    url = base_url + BASE_PATH
    payload = {"ingredients": ["invalid_hash_123"]}
    resp = requests.post(url, json=payload, headers=auth_header)
    assert resp.status_code == 500
