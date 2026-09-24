def register(client, email: str = "owner@example.com") -> dict:
    response = client.post(
        "/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "password": "strong-password",
            "confirm_password": "strong-password",
        },
    )
    assert response.status_code == 201
    return response.json()


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def room_payload() -> dict:
    return {
        "room_name": "Living Room",
        "current_room_type": "living_room",
        "room_shape": "rectangle",
        "room_layout_type": "closed",
        "room_size": 24.0,
        "ceiling_height": 2.7,
        "wall_count": 4,
    }


def test_register_login_and_authenticated_profile(client):
    registration = register(client)
    token = registration["access_token"]

    me = client.get("/users/me", headers=auth_header(token))
    assert me.status_code == 200
    assert me.json()["email"] == "owner@example.com"

    login = client.post(
        "/auth/login",
        json={"email": "owner@example.com", "password": "strong-password"},
    )
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["access_token"]


def test_invalid_token_is_rejected(client):
    response = client.get("/users/me", headers=auth_header("not-a-valid-token"))
    assert response.status_code == 401


def test_room_access_is_scoped_to_authenticated_owner(client):
    owner = register(client, "owner@example.com")
    other = register(client, "other@example.com")

    created = client.post(
        "/rooms",
        headers=auth_header(owner["access_token"]),
        json=room_payload(),
    )
    assert created.status_code == 201
    room_id = created.json()["id"]

    visible = client.get(
        f"/rooms/{room_id}", headers=auth_header(owner["access_token"])
    )
    assert visible.status_code == 200

    hidden = client.get(
        f"/rooms/{room_id}", headers=auth_header(other["access_token"])
    )
    assert hidden.status_code == 404
