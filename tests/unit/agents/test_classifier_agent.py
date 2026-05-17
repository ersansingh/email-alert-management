import pytest
import os
import importlib
os.environ["LLM_BASE_URL"] = "http://mock-llm:5000"

import pytest
from unittest.mock import patch, MagicMock
from app.agents.state import AlertState
import app.agents.classifier_agent as classifier_module

@patch("app.agents.classifier_agent.ChatOpenAI.invoke")
def test_classifier_agent(mock_invoke):
    mock_response = MagicMock()
    mock_response.content = "hardware_failure"
    mock_invoke.return_value = mock_response

    state = AlertState(message="Server is down")
    res = classifier_module.classifier_agent(state)

    assert res["alert_type"] == "hardware_failure"
    mock_invoke.assert_called_once()

@patch.dict(os.environ, {"LLM_BASE_URL": "http://mock-llm:5000"})
def test_classifier_agent_base_url_append_v1():
    # Reload the module to trigger the LLM_BASE_URL logic
    importlib.reload(classifier_module)
    assert classifier_module.llm_base_url == "http://mock-llm:5000/v1"


