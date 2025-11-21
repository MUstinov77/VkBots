from http.client import responses

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth.schemas import UserSignupLoginSchema
from .fixtures import lifespan
from app.main import app

client = TestClient(app)



users = [
    UserSignupLoginSchema(
        username="max",
        password="123"
    ),

]
user = UserSignupLoginSchema(
    username="amx",
    password="123"
)

def test_create_user(lifespan):
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