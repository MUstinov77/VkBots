from fastapi.testclient import TestClient

from backend.app.api.auth.schemas import UserSignupLoginSchema
from backend.app.main import app

from .fixtures import lifespan, engine

client = TestClient(app)


def test_create_user(lifespan, engine):
    response = client.post(
        "/auth/signup",
        json={"username": "max", "password": "123"}
    )


    assert response.status_code == 201
    assert response.json() == {"message": "User created"}

def test_login(lifespan):
    client.post(
        "/auth/signup",
        json={"username": "max", "password": "123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "max", "password": "123"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"