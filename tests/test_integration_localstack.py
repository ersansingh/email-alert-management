import pytest
import boto3
from testcontainers.localstack import LocalStackContainer
from app.agents.state import AlertState

@pytest.fixture(scope="module")
def localstack():
    with LocalStackContainer(image="localstack/localstack:3.0.2") as localstack:
        yield localstack

@pytest.fixture
def s3_client(localstack):
    return boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url=localstack.get_url()
    )

@pytest.fixture
def sqs_client(localstack):
    return boto3.client(
        "sqs",
        region_name="us-east-1",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint_url=localstack.get_url()
    )

def test_s3_integration(s3_client):
    bucket_name = "test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key="test.txt", Body="hello localstack")
    
    response = s3_client.get_object(Bucket=bucket_name, Key="test.txt")
    assert response["Body"].read().decode("utf-8") == "hello localstack"

def test_sqs_integration(sqs_client):
    queue_name = "test-queue"
    sqs_client.create_queue(QueueName=queue_name)
    queue_url = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]
    
    sqs_client.send_message(QueueUrl=queue_url, MessageBody="test-message")
    
    response = sqs_client.receive_message(QueueUrl=queue_url)
    assert response["Messages"][0]["Body"] == "test-message"
