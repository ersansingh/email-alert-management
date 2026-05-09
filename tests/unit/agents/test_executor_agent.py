import pytest
from unittest.mock import patch, MagicMock
from app.agents.state import AlertState
from app.agents.executor_agent import executor_agent

@patch("app.agents.executor_agent.subprocess.run")
def test_executor_agent_success(mock_run):
    # Mock subprocess.run to return a successful CompletedProcess
    mock_out = MagicMock()
    mock_out.returncode = 0
    mock_run.return_value = mock_out

    state = AlertState(
        message="test",
        remediation_plan=[{"step": "test step", "action": "echo test"}]
    )
    
    res = executor_agent(state)
    
    assert "execution_status" in res
    assert "test step" in res["execution_status"]
    assert "'status': 0" in res["execution_status"]
    mock_run.assert_called_once_with("echo test", shell=True, capture_output=True)

@patch("app.agents.executor_agent.subprocess.run")
def test_executor_agent_exception(mock_run):
    # Mock subprocess.run to raise an exception
    mock_run.side_effect = Exception("Command failed")

    state = AlertState(
        message="test",
        remediation_plan=[{"step": "test step", "action": "fail command"}]
    )
    
    res = executor_agent(state)
    
    assert "execution_status" in res
    assert "Command failed" in res["execution_status"]
    mock_run.assert_called_once_with("fail command", shell=True, capture_output=True)

def test_executor_agent_empty_plan():
    state = AlertState(
        message="test",
        remediation_plan=[]
    )
    res = executor_agent(state)
    assert res["execution_status"] == "[]"
