import requests


class PetService:
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url
        self.session = session
        self.endpoint = f"{self.base_url}/pet"

    def add_pet(self, payload: dict) -> requests.Response:
        return self.session.post(self.endpoint, json=payload)

    def get_pet(self, pet_id: int) -> requests.Response:
        return self.session.get(f"{self.endpoint}/{pet_id}")

    def update_pet(self, payload: dict) -> requests.Response:
        return self.session.put(self.endpoint, json=payload)

    def delete_pet(self, pet_id: int) -> requests.Response:
        return self.session.delete(f"{self.endpoint}/{pet_id}")

    def find_by_status(self, status: str) -> requests.Response:
        return self.session.get(f"{self.endpoint}/findByStatus", params={"status": status})
