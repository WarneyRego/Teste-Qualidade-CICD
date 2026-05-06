import json

USER_PAYLOAD = {
    "id": 112233445,
    "username": "testuser_cicd",
    "firstName": "Test",
    "lastName": "User",
    "email": "testuser_cicd@example.com",
    "password": "securepass123",
    "phone": "11999999999",
    "userStatus": 1,
}


def _log(method, url, status, body):
    print(f"  {method} {url}")
    print(f"  Status: {status}")
    print(f"  Response: {json.dumps(body, indent=4)}")


def test_create_user(user_service):
    print(f"Criar usuário '{USER_PAYLOAD['username']}'")
    response = user_service.create_user(USER_PAYLOAD)
    body = response.json()
    _log("POST", "/user", response.status_code, body)

    assert response.status_code == 200
    assert str(USER_PAYLOAD["id"]) == body.get("message")


def test_get_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    print(f"Buscar usuário '{USER_PAYLOAD['username']}'")
    response = user_service.get_user(USER_PAYLOAD["username"])
    body = response.json()
    _log("GET", f"/user/{USER_PAYLOAD['username']}", response.status_code, body)

    assert response.status_code == 200
    assert body["username"] == USER_PAYLOAD["username"]
    assert body["email"] == USER_PAYLOAD["email"]


def test_update_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    print(f"Atualizar firstName e email do usuário '{USER_PAYLOAD['username']}'")
    updated = {**USER_PAYLOAD, "firstName": "Updated", "email": "updated@example.com"}
    response = user_service.update_user(USER_PAYLOAD["username"], updated)
    _log("PUT", f"/user/{USER_PAYLOAD['username']}", response.status_code, response.json())

    assert response.status_code == 200

    get_response = user_service.get_user(USER_PAYLOAD["username"])
    body = get_response.json()
    print(f"  Verificação GET após update: firstName={body['firstName']}, email={body['email']}")
    assert body["firstName"] == "Updated"
    assert body["email"] == "updated@example.com"


def test_user_login(user_service):
    user_service.create_user(USER_PAYLOAD)
    print(f"Login com usuário '{USER_PAYLOAD['username']}'")
    response = user_service.login(USER_PAYLOAD["username"], USER_PAYLOAD["password"])
    body = response.json()
    _log("GET", f"/user/login?username={USER_PAYLOAD['username']}", response.status_code, body)

    assert response.status_code == 200
    assert "logged in" in body.get("message", "").lower()


def test_delete_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    print(f"Deletar usuário '{USER_PAYLOAD['username']}' e confirmar remoção")
    response = user_service.delete_user(USER_PAYLOAD["username"])
    _log("DELETE", f"/user/{USER_PAYLOAD['username']}", response.status_code, response.json())

    assert response.status_code == 200

    get_response = user_service.get_user(USER_PAYLOAD["username"])
    print(f"  GET após delete → Status: {get_response.status_code} (esperado 404)")
    assert get_response.status_code == 404


def test_get_nonexistent_user_returns_404(user_service):
    print("Buscar usuário inexistente — deve retornar 404")
    response = user_service.get_user("user_that_does_not_exist_xyz123")
    _log("GET", "/user/user_that_does_not_exist_xyz123", response.status_code, response.json())

    assert response.status_code == 404
