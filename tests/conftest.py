import os
import pytest
from pydantic import BaseModel

class TestConfig(BaseModel):
    env_name: str
    base_url: str
    project_id: str = "ai-learning-495017"
    region: str = "us-central1"
    
    @property
    def is_gcp(self):
        return self.env_name == "gcpprod"
    
    @property
    def is_aws(self):
        return self.env_name == "awsprod"

@pytest.fixture(scope="session")
def config():
    env = os.environ.get("ENV_NAME", "local")
    base_url = os.environ.get("BASE_URL", "http://localhost:8000")
    
    return TestConfig(
        env_name=env,
        base_url=base_url
    )
