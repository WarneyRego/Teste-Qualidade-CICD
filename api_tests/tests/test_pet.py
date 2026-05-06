import pytest

PET_PAYLOAD = {
    "id": 987654321,
    "category": {"id": 1, "name": "Dogs"},
    "name": "Rex",
    "photoUrls": ["https://example.com/rex.jpg"],
    "tags": [{"id": 1, "name": "trained"}],
    "status": "available",
}


def test_add_pet(pet_service):
    response = pet_service.add_pet(PET_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == PET_PAYLOAD["id"]
    assert body["name"] == "Rex"
    assert body["status"] == "available"


def test_get_pet_by_id(pet_service):
    response = pet_service.get_pet(PET_PAYLOAD["id"])

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == PET_PAYLOAD["id"]
    assert body["name"] == "Rex"


def test_update_pet(pet_service):
    updated = {**PET_PAYLOAD, "name": "Rex Updated", "status": "sold"}
    response = pet_service.update_pet(updated)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Rex Updated"
    assert body["status"] == "sold"


def test_find_pets_by_status(pet_service):
    response = pet_service.find_by_status("available")

    assert response.status_code == 200
    pets = response.json()
    assert isinstance(pets, list)
    assert len(pets) > 0
    # Every returned pet must carry the requested status
    for pet in pets[:10]:
        assert pet.get("status") == "available"


def test_delete_pet(pet_service):
    # Re-create to guarantee the pet exists before deletion
    pet_service.add_pet(PET_PAYLOAD)
    response = pet_service.delete_pet(PET_PAYLOAD["id"])

    assert response.status_code == 200

    # Confirm the pet is gone
    get_response = pet_service.get_pet(PET_PAYLOAD["id"])
    assert get_response.status_code == 404


def test_get_nonexistent_pet_returns_404(pet_service):
    response = pet_service.get_pet(999999999999)

    assert response.status_code == 404
