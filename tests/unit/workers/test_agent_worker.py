import pytest
from unittest.mock import patch
from app.workers.agent_worker import process_alert

@patch("app.workers.agent_worker.graph.invoke")
def test_process_alert(mock_graph_invoke):
    payload = {"message": "Test alert"}
    mock_graph_invoke.return_value = {"status": "success", "resolved": True}

    result = process_alert(payload)

    mock_graph_invoke.assert_called_once_with(payload)
    assert result == {"status": "success", "resolved": True}
