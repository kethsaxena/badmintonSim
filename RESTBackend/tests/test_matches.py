import pytest
from fastapi.testclient import TestClient
from main import app
from projEnums import matchStatus
client = TestClient(app)

def test_create_match():
    response = client.post("/creatematch")
    assert response.status_code == 200
    data = response.json()
    assert "matchid" in data
    assert data["status"] == matchStatus.IP
