import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def register_user(self, email: str, password: str, name: str | None = None):
        url = f"{self.base_url}/api/auth/register"
        payload = {
            "email": email,
            "password": password
        }
        
        
        if name is not None:
            payload["name"] = name
            
        response = requests.post(url, json=payload)
        return response
