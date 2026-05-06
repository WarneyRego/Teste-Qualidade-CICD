import requests


class StoreService:
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session
        self.endpoint = f"{self.base_url}/store"

    def get_inventory(self) -> requests.Response:
        return self.session.get(f"{self.endpoint}/inventory")

    def place_order(self, payload: dict) -> requests.Response:
        return self.session.post(f"{self.endpoint}/order", json=payload)

    def get_order(self, order_id: int) -> requests.Response:
        return self.session.get(f"{self.endpoint}/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        return self.session.delete(f"{self.endpoint}/order/{order_id}")
