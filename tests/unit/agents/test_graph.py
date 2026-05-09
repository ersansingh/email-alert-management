from app.agents.graph import builder, graph
from unittest.mock import patch, MagicMock

def test_graph_lambdas():
    pass

@patch("app.agents.classifier_agent.ChatOpenAI.invoke")
@patch("app.agents.executor_agent.subprocess.run")
def test_graph_execution_auto_remediate(mock_run, mock_llm_invoke):
    mock_response = MagicMock()
    mock_response.content = "test_type"
    mock_llm_invoke.return_value = mock_response

    mock_out = MagicMock()
    mock_out.returncode = 0
    mock_run.return_value = mock_out
    
    # State with critical triggers auto_remediate route -> planner -> approval -> executor -> validator -> learning
    state = {"message": "Test", "severity": "critical"}
    result = graph.invoke(state)
    
    assert result["decision"] == "auto_remediate"
    assert result["validation_status"] == "resolved"
    assert "execution_status" in result
    mock_llm_invoke.assert_called_once()
    mock_run.assert_called_once()

@patch("app.agents.classifier_agent.ChatOpenAI.invoke")
def test_graph_execution_notify(mock_llm_invoke):
    mock_response = MagicMock()
    mock_response.content = "test_type"
    mock_llm_invoke.return_value = mock_response
    
    # State with low triggers notify route -> learning directly
    state = {"message": "Test", "severity": "low"}
    result = graph.invoke(state)
    
    assert result["decision"] == "notify"
    assert "validation_status" not in result # Doesn't go to validator
    mock_llm_invoke.assert_called_once()


