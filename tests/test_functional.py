import requests
import pytest
import time
import boto3

BASE_URL = "http://localhost:8000"
AWS_ENDPOINT = "http://localhost:4566"

def test_health_check():
    # FastAPI doesn't have a default health check, but we can check if it's up
    try:
        response = requests.get(f"{BASE_URL}/metrics")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail("Service is not running")

def test_alert_processing():
    payload = {
        "message": "High CPU usage on production-api-01",
        "severity": "critical"
    }
    response = requests.post(f"{BASE_URL}/alert", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "processed"
    assert "result" in data
    assert "alert_type" in data["result"]
    assert "remediation_plan" in data["result"]

def test_infrastructure_provisioned():
    s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT, aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")
    sqs = boto3.client("sqs", endpoint_url=AWS_ENDPOINT, aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")
    
    # Check S3 bucket
    buckets = s3.list_buckets()
    bucket_names = [b["Name"] for b in buckets["Buckets"]]
    assert any("ai-sre-alert-archive" in name for name in bucket_names)
    
    # Check SQS queue
    queues = sqs.list_queues()
    queue_urls = queues.get("QueueUrls", [])
    assert any("ai-sre-alerts-queue" in url for url in queue_urls)
