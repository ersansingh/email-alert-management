import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classifier_endpoint():
    payload = {"message": "Test alert"}
    response = client.post("/agents/classifier", json=payload)
    assert response.status_code == 200
    assert "alert_type" in response.json()
