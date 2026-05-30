import pytest
import boto3

@pytest.fixture
def s3_client(config):
    if not config.is_aws:
        pytest.skip("AWS tests only")
    return boto3.client("s3", region_name="us-east-1")

@pytest.fixture
def sqs_client(config):
    if not config.is_aws:
        pytest.skip("AWS tests only")
    return boto3.client("sqs", region_name="us-east-1")

def test_s3_infrastructure(s3_client):
    """Verify that the S3 bucket for alert archiving exists."""
    bucket_name = "ai-sre-alert-archive-us-east-1"
    response = s3_client.list_buckets()
    bucket_names = [b["Name"] for b in response["Buckets"]]
    assert any(bucket_name in name for name in bucket_names)

def test_sqs_infrastructure(sqs_client):
    """Verify that the SQS queue for alerts exists."""
    queue_name = "ai-sre-alerts-queue"
    response = sqs_client.get_queue_url(QueueName=queue_name)
    assert "QueueUrl" in response
