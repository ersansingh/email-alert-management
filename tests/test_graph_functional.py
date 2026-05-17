import pytest
import pytest
from unittest.mock import patch, MagicMock
from app.agents.state import AlertState

@patch("app.agents.classifier_agent.llm")
def test_graph_initialization(mock_llm):
    mock_response = MagicMock()
    mock_response.content = "hardware_failure"
    mock_llm.invoke.return_value = mock_response

    from app.agents.graph import graph
    initial_state = AlertState(message="Test alert")
    result = graph.invoke(initial_state)
    assert result is not None
    assert "alert_type" in result
