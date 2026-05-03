import pytest
from app.agents.graph import graph
from app.agents.state import AlertState

def test_graph_initialization():
    initial_state = AlertState(message="Test alert")
    result = graph.invoke(initial_state)
    assert result is not None
    assert "alert_type" in result
