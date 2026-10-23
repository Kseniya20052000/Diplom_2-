import pytest
import requests
import uuid

@pytest.fixture(scope="function")
def base_url():
    return "https://stellarburgers.education-services.ru"

@pytest.fixture(scope="function")
def registered_user(base_url):
    unique_email = f"test_auto_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": unique_email, "password": "12345", "name": "Auto User"}
    resp = requests.post(f"{base_url}/api/users/", json=payload)
    if resp.status_code in (200, 409):
        return payload
    raise RuntimeError(f"Failed to prepare user: {resp.status_code}")

@pytest.fixture(scope="function")
def auth_header(registered_user, base_url):
    login_resp = requests.post(
        f"{base_url}/api/auth/login",
        json={"email": registered_user["email"], "password": registered_user["password"]}
    )
    token = login_resp.json()["accessToken"]
    return {"authorization": f"Bearer {token}"}
