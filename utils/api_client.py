import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def register_user(self, email: str, password: str, name: str | None = None):
        url = f"{self.base_url}/api/auth/register"
        payload = {"email": email, "password": password}
        if name is not None:
            payload["name"] = name
        return requests.post(url, json=payload)

    def login_user(self, email: str, password: str):
        url = f"{self.base_url}/api/auth/login"
        payload = {"email": email, "password": password}
        return requests.post(url, json=payload)

    def logout_user(self, refresh_token: str):
        url = f"{self.base_url}/api/auth/logout"
        payload = {"token": refresh_token}
        return requests.post(url, json=payload)

    def refresh_token(self, refresh_token: str):
        url = f"{self.base_url}/api/auth/token"
        payload = {"token": refresh_token}
        return requests.post(url, json=payload)

    def get_ingredients(self):
        url = f"{self.base_url}/api/ingredients"
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        ingredients = data.get("data", )
        if len(ingredients) < 2:
            raise RuntimeError("Недостаточно ингредиентов в базе для теста")
        return [ing["_id"] for ing in ingredients[:2]]


    def create_order(self, ingredients: list[str], access_token: str | None = None):
        url = f"{self.base_url}/api/orders"
        payload = {"ingredients": ingredients}
        
        headers = {}
        if access_token:
            
            headers["Authorization"] = f"Bearer {access_token}"
        
        return requests.post(url, json=payload, headers=headers)
