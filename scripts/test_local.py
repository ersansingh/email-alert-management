import pytest
import boto3
import os
import time
from testcontainers.localstack import LocalStackContainer

# This script is intended for local development testing using Docker Desktop.
# It uses testcontainers to spin up a transient LocalStack instance.

@pytest.fixture(scope="module")
def localstack():
    """Start a LocalStack container for the duration of the test module."""
    # Ensure Docker Desktop is running before starting this test
    with LocalStackContainer(image="localstack/localstack:3.0.2") as localstack:
        # Wait a moment for services to initialize internally
        time.sleep(5)
        yield localstack

@pytest.fixture
def s3_client(localstack):
    """S3 client pointing to the localstack instance."""
    return boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url=localstack.get_url()
    )

@pytest.fixture
def sqs_client(localstack):
    """SQS client pointing to the localstack instance."""
    return boto3.client(
        "sqs",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url=localstack.get_url()
    )

def test_local_s3_integration(s3_client):
    """Test S3 operations against localstack."""
    bucket_name = "test-local-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key="local-test.txt", Body="hello from local script")
    
    response = s3_client.get_object(Bucket=bucket_name, Key="local-test.txt")
    content = response["Body"].read().decode("utf-8")
    print(f"\nS3 Read Content: {content}")
    assert content == "hello from local script"

def test_local_sqs_integration(sqs_client):
    """Test SQS operations against localstack."""
    queue_name = "test-local-queue"
    sqs_client.create_queue(QueueName=queue_name)
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    
    sqs_client.send_message(QueueUrl=queue_url, MessageBody="local-test-message")
    
    response = sqs_client.receive_message(QueueUrl=queue_url)
    message_body = response["Messages"][0]["Body"]
    print(f"\nSQS Received Message: {message_body}")
    assert message_body == "local-test-message"

if __name__ == "__main__":
    # Prevent execution in CI environments
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print("This script is for local use only and cannot be run in GitHub Actions.")
        exit(0)
        
    # Allow running directly via 'python scripts/test_local.py'
    # Sets ENV_NAME to local for consistency
    os.environ["ENV_NAME"] = "local"
    pytest.main([__file__, "-v", "-s"])
