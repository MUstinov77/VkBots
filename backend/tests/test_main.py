from fastapi import status
from fastapi.responses import Response
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)

def test_main_entry_point():
    response = client.get("/")
    exp_response = Response(content="VkBot app api", status_code=status.HTTP_200_OK)
    assert response.status_code == exp_response.status_code
    assert response.content == exp_response.body
    