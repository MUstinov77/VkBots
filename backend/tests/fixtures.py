import pytest
from fastapi.testclient import TestClient

from backend.app.core.utils.lifespan import drop_db, engine, init_db
from backend.app.main import app


@pytest.fixture
def lifespan():
    init_db()
    yield
    drop_db()
    engine.dispose()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def test_user_data():
    return {
        "username": "ajax",
        "password": "123"
    }

@pytest.fixture
def create_user(
    lifespan,
    client,
    test_user_data
):
    response = client.post(
        "/auth/signup",
        json=test_user_data
    )
    return response.json()

@pytest.fixture
def get_user_access_token(
    client,
    create_user,
    test_user_data,
):
    response = client.post(
        "/auth/login",
        data=test_user_data
    )
    return response.json().get("access_token")

