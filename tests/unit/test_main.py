import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.main.process_alert")
def test_handle_alert_success(mock_process):
    mock_process.return_value = {"mock": "result"}
    
    response = client.post("/alert", json={"message": "CPU is high"})
    
    assert response.status_code == 200
    assert response.json() == {"status": "processed", "result": {"mock": "result"}}
    mock_process.assert_called_once_with({"message": "CPU is high"})

@patch("app.main.process_alert")
def test_handle_alert_exception(mock_process):
    mock_process.side_effect = Exception("Mock processing error")
    
    with pytest.raises(Exception) as exc_info:
        client.post("/alert", json={"message": "CPU is high"})
        
    assert "Mock processing error" in str(exc_info.value)
    mock_process.assert_called_once()

def test_metrics_endpoint():
    response = client.get("/metrics")
    # Prometheus might redirect /metrics to /metrics/ 
    # but Starlette mount typically handles it, check 200
    assert response.status_code in [200, 307]
