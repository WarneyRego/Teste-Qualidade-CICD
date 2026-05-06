import requests


class UserService:
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session
        self.endpoint = f"{self.base_url}/user"

    def create_user(self, payload: dict) -> requests.Response:
        return self.session.post(self.endpoint, json=payload)

    def get_user(self, username: str) -> requests.Response:
        return self.session.get(f"{self.endpoint}/{username}")

    def update_user(self, username: str, payload: dict) -> requests.Response:
        return self.session.put(f"{self.endpoint}/{username}", json=payload)

    def delete_user(self, username: str) -> requests.Response:
        return self.session.delete(f"{self.endpoint}/{username}")

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.get(
            f"{self.endpoint}/login",
            params={"username": username, "password": password},
        )
