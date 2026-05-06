import pytest

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


def test_create_user(user_service):
    response = user_service.create_user(USER_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    # The API echoes back the created user's id as message
    assert str(USER_PAYLOAD["id"]) == body.get("message")


def test_get_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    response = user_service.get_user(USER_PAYLOAD["username"])

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == USER_PAYLOAD["username"]
    assert body["email"] == USER_PAYLOAD["email"]


def test_update_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    updated = {**USER_PAYLOAD, "firstName": "Updated", "email": "updated@example.com"}
    response = user_service.update_user(USER_PAYLOAD["username"], updated)

    assert response.status_code == 200

    get_response = user_service.get_user(USER_PAYLOAD["username"])
    body = get_response.json()
    assert body["firstName"] == "Updated"
    assert body["email"] == "updated@example.com"


def test_user_login(user_service):
    user_service.create_user(USER_PAYLOAD)
    response = user_service.login(USER_PAYLOAD["username"], USER_PAYLOAD["password"])

    assert response.status_code == 200
    body = response.json()
    # A successful login returns a session token in the message field
    assert "logged in" in body.get("message", "").lower()


def test_delete_user(user_service):
    user_service.create_user(USER_PAYLOAD)
    response = user_service.delete_user(USER_PAYLOAD["username"])

    assert response.status_code == 200

    get_response = user_service.get_user(USER_PAYLOAD["username"])
    assert get_response.status_code == 404


def test_get_nonexistent_user_returns_404(user_service):
    response = user_service.get_user("user_that_does_not_exist_xyz123")

    assert response.status_code == 404
