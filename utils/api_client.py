import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def register_user(self, email: str, password: str, name: str):
        url = f"{self.base_url}/api/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(url, json=payload)
        return response
