from app.agents.state import AlertState
from app.agents.approval_agent import approval_agent
from app.agents.decision_agent import decision_agent
from app.agents.learning_agent import learning_agent
from app.agents.planner_agent import planner_agent
from app.agents.retriever_agent import retriever_agent
from app.agents.validator_agent import validator_agent

def test_approval_agent():
    state = AlertState(message="test")
    res = approval_agent(state)
    assert res == {"approved": True}

def test_decision_agent_critical():
    state = AlertState(message="test", severity="critical")
    res = decision_agent(state)
    assert res == {"decision": "auto_remediate"}

def test_decision_agent_notify():
    state = AlertState(message="test", severity="low")
    res = decision_agent(state)
    assert res == {"decision": "notify"}

def test_learning_agent():
    state = AlertState(message="test", severity="low")
    res = learning_agent(state)
    assert res == state

def test_planner_agent():
    state = AlertState(message="test")
    res = planner_agent(state)
    assert "remediation_plan" in res
    assert len(res["remediation_plan"]) == 1
    assert res["remediation_plan"][0]["step"] == "restart service"

def test_retriever_agent():
    state = AlertState(message="test")
    res = retriever_agent(state)
    assert "similar_incidents" in res
    assert res["similar_incidents"][0]["fix"] == "restart service"

def test_validator_agent():
    state = AlertState(message="test")
    res = validator_agent(state)
    assert res == {"validation_status": "resolved"}
