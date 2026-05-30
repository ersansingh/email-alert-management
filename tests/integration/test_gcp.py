import pytest
from google.cloud import storage
from google.cloud import pubsub_v1

@pytest.fixture
def storage_client(config):
    if not config.is_gcp:
        pytest.skip("GCP tests only")
    return storage.Client(project=config.project_id)

@pytest.fixture
def pubsub_client(config):
    if not config.is_gcp:
        pytest.skip("GCP tests only")
    return pubsub_v1.PublisherClient()

def test_gcs_infrastructure(storage_client, config):
    """Verify that the GCS bucket for alert archiving exists."""
    bucket_name = f"ai-sre-alert-archive-{config.region}"
    bucket = storage_client.get_bucket(bucket_name)
    assert bucket.exists()

def test_pubsub_infrastructure(pubsub_client, config):
    """Verify that the Pub/Sub topic for alerts exists."""
    topic_id = "ai-sre-alerts-topic"
    topic_path = pubsub_client.topic_path(config.project_id, topic_id)
    topic = pubsub_client.get_topic(request={"topic": topic_path})
    assert topic.name == topic_path
