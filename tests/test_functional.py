import requests
import pytest

# Application functionality tests focusing on end-to-end alert processing
# Boilerplate/Configuration is injected via the 'config' fixture in conftest.py

def test_app_health(config):
    """Verify the application API is reachable in the current environment."""
    response = requests.get(f"{config.base_url}/metrics")
    assert response.status_code == 200

def test_critical_alert_processing(config):
    """Test full workflow for a critical alert requiring auto-remediation."""
    payload = {
        "message": "Critical: Database connection pool exhausted on prod-db-01",
        "severity": "critical",
        "metadata": {"host": "prod-db-01", "service": "postgresql"}
    }
    response = requests.post(f"{config.base_url}/alert", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "processed"
    
    result = data["result"]
    # Verify the graph reached the expected final states
    # Note: These keys depend on the agent outputs in app/agents/
    assert "alert_type" in result
    assert "remediation_plan" in result
    assert "execution_status" in result

def test_low_severity_alert_processing(config):
    """Test workflow for a low severity alert that might skip execution."""
    payload = {
        "message": "Warning: Disk usage at 75% on staging-web-02",
        "severity": "low"
    }
    response = requests.post(f"{config.base_url}/alert", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "processed"
    # Low severity might skip certain nodes in a real scenario
    assert "alert_type" in data["result"]
