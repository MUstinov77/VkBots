from fastapi.testclient import TestClient

from backend.app.main import app

from .fixtures import lifespan, test_user_data

client = TestClient(app)


def test_get_bots_by_authorized_user(lifespan, test_user_data):
    client.post(
        "/auth/signup",
        json=test_user_data,
    )
    access_token = client.post(
        "/auth/login",
        data=test_user_data,
    ).json().get("access_token")
    response = client.get(
        "/bots",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200


def test_create_bot_by_authorized_user(lifespan, test_user_data):
    client.post(
        "/auth/signup",
        json=test_user_data,
    )
    access_token = client.post(
        "/auth/login",
        data=test_user_data,
    ).json().get("access_token")
    response = client.post(
        "/bots",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "login": "login",
            "password": "password",
            "env": "prod",
            "domain": "canary"
        },
    )

    assert response.status_code == 201
    assert response.json() == {"message": "Bot created"}

def test_create_bot_by_unauthorized_user():
    response = client.post(
        "/bots",
        json={
            "login": "login",
            "password": "password",
            "env": "prod",
            "domain": "canary"
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
