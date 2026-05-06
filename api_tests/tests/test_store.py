import pytest

ORDER_PAYLOAD = {
    "id": 123456789,
    "petId": 987654321,
    "quantity": 2,
    "shipDate": "2024-01-15T10:00:00.000Z",
    "status": "placed",
    "complete": False,
}


def test_get_inventory(store_service):
    response = store_service.get_inventory()

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    # The inventory response is a map of status → quantity; at minimum it should not be empty
    assert len(body) > 0


def test_place_order(store_service):
    response = store_service.place_order(ORDER_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == ORDER_PAYLOAD["id"]
    assert body["petId"] == ORDER_PAYLOAD["petId"]
    assert body["status"] == "placed"


def test_get_order_by_id(store_service):
    # Ensure the order exists first
    store_service.place_order(ORDER_PAYLOAD)
    response = store_service.get_order(ORDER_PAYLOAD["id"])

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == ORDER_PAYLOAD["id"]
    assert body["quantity"] == ORDER_PAYLOAD["quantity"]


def test_delete_order(store_service):
    store_service.place_order(ORDER_PAYLOAD)
    response = store_service.delete_order(ORDER_PAYLOAD["id"])

    assert response.status_code == 200

    # Order must no longer be retrievable
    get_response = store_service.get_order(ORDER_PAYLOAD["id"])
    assert get_response.status_code == 404


def test_get_nonexistent_order_returns_404(store_service):
    response = store_service.get_order(999999999999)

    assert response.status_code == 404
