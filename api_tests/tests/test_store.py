import json

ORDER_PAYLOAD = {
    "id": 123456789,
    "petId": 987654321,
    "quantity": 2,
    "shipDate": "2024-01-15T10:00:00.000Z",
    "status": "placed",
    "complete": False,
}


def _log(method, url, status, body):
    print(f"  {method} {url}")
    print(f"  Status: {status}")
    print(f"  Response: {json.dumps(body, indent=4)}")


def test_get_inventory(store_service):
    print("Consultar inventário da loja")
    response = store_service.get_inventory()
    body = response.json()
    print(f"  GET /store/inventory")
    print(f"  Status: {response.status_code}")
    print(f"  Categorias no inventário: {list(body.keys())[:8]}")
    print(f"  Response (primeiras 5 chaves): {json.dumps(dict(list(body.items())[:5]), indent=4)}")

    assert response.status_code == 200
    assert isinstance(body, dict)
    assert len(body) > 0


def test_place_order(store_service):
    print("Criar novo pedido")
    response = store_service.place_order(ORDER_PAYLOAD)
    body = response.json()
    _log("POST", "/store/order", response.status_code, body)

    assert response.status_code == 200
    assert body["id"] == ORDER_PAYLOAD["id"]
    assert body["petId"] == ORDER_PAYLOAD["petId"]
    assert body["status"] == "placed"


def test_get_order_by_id(store_service):
    store_service.place_order(ORDER_PAYLOAD)
    print(f"Buscar pedido ID {ORDER_PAYLOAD['id']}")
    response = store_service.get_order(ORDER_PAYLOAD["id"])
    body = response.json()
    _log("GET", f"/store/order/{ORDER_PAYLOAD['id']}", response.status_code, body)

    assert response.status_code == 200
    assert body["id"] == ORDER_PAYLOAD["id"]
    assert body["quantity"] == ORDER_PAYLOAD["quantity"]


def test_delete_order(store_service):
    store_service.place_order(ORDER_PAYLOAD)
    print(f"Deletar pedido ID {ORDER_PAYLOAD['id']} e confirmar remoção")
    response = store_service.delete_order(ORDER_PAYLOAD["id"])
    _log("DELETE", f"/store/order/{ORDER_PAYLOAD['id']}", response.status_code, response.json())

    assert response.status_code == 200

    get_response = store_service.get_order(ORDER_PAYLOAD["id"])
    print(f"  GET após delete → Status: {get_response.status_code} (esperado 404)")
    assert get_response.status_code == 404


def test_get_nonexistent_order_returns_404(store_service):
    print("Buscar pedido inexistente — deve retornar 404")
    response = store_service.get_order(999999999999)
    _log("GET", "/store/order/999999999999", response.status_code, response.json())

    assert response.status_code == 404
