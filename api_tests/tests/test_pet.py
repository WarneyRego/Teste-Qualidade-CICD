import json

PET_PAYLOAD = {
    "id": 987654321,
    "category": {"id": 1, "name": "Dogs"},
    "name": "Rex",
    "photoUrls": ["https://example.com/rex.jpg"],
    "tags": [{"id": 1, "name": "trained"}],
    "status": "available",
}


def _log(method, url, status, body):
    print(f"  {method} {url}")
    print(f"  Status: {status}")
    print(f"  Response: {json.dumps(body, indent=4)}")


def test_add_pet(pet_service):
    print("Cadastrar novo pet (Rex)")
    response = pet_service.add_pet(PET_PAYLOAD)
    body = response.json()
    _log("POST", "/pet", response.status_code, body)

    assert response.status_code == 200
    assert body["id"] == PET_PAYLOAD["id"]
    assert body["name"] == "Rex"
    assert body["status"] == "available"


def test_get_pet_by_id(pet_service):
    print(f"Buscar pet pelo ID {PET_PAYLOAD['id']}")
    response = pet_service.get_pet(PET_PAYLOAD["id"])
    body = response.json()
    _log("GET", f"/pet/{PET_PAYLOAD['id']}", response.status_code, body)

    assert response.status_code == 200
    assert body["id"] == PET_PAYLOAD["id"]
    assert body["name"] == "Rex"


def test_update_pet(pet_service):
    print("Atualizar nome e status do pet")
    updated = {**PET_PAYLOAD, "name": "Rex Updated", "status": "sold"}
    response = pet_service.update_pet(updated)
    body = response.json()
    _log("PUT", "/pet", response.status_code, body)

    assert response.status_code == 200
    assert body["name"] == "Rex Updated"
    assert body["status"] == "sold"


def test_find_pets_by_status(pet_service):
    print("Listar pets com status=available")
    response = pet_service.find_by_status("available")
    pets = response.json()
    sample = pets[:3]
    print(f"  GET /pet/findByStatus?status=available")
    print(f"  Status: {response.status_code}")
    print(f"  Total retornado: {len(pets)} pets")
    print(f"  Primeiros 3: {json.dumps(sample, indent=4)}")

    assert response.status_code == 200
    assert isinstance(pets, list)
    assert len(pets) > 0
    for pet in pets[:10]:
        assert pet.get("status") == "available"


def test_delete_pet(pet_service):
    print(f"Deletar pet ID {PET_PAYLOAD['id']} e confirmar remoção")
    pet_service.add_pet(PET_PAYLOAD)
    response = pet_service.delete_pet(PET_PAYLOAD["id"])
    _log("DELETE", f"/pet/{PET_PAYLOAD['id']}", response.status_code, response.json())

    assert response.status_code == 200

    get_response = pet_service.get_pet(PET_PAYLOAD["id"])
    print(f"  GET após delete → Status: {get_response.status_code} (esperado 404)")
    assert get_response.status_code == 404


def test_get_nonexistent_pet_returns_404(pet_service):
    print("Buscar pet inexistente — deve retornar 404")
    response = pet_service.get_pet(999999999999)
    _log("GET", "/pet/999999999999", response.status_code, response.json())

    assert response.status_code == 404
