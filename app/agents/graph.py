from langgraph.graph import StateGraph

from app.agents.classifier_agent import classifier_agent
from app.agents.retriever_agent import retriever_agent
from app.agents.decision_agent import decision_agent
from app.agents.planner_agent import planner_agent
from app.agents.approval_agent import approval_agent
from app.agents.executor_agent import executor_agent
from app.agents.validator_agent import validator_agent
from app.agents.learning_agent import learning_agent

builder = StateGraph(dict)

builder.add_node("classifier", classifier_agent)
builder.add_node("retriever", retriever_agent)
builder.add_node("decision", decision_agent)
builder.add_node("planner", planner_agent)
builder.add_node("approval", approval_agent)
builder.add_node("executor", executor_agent)
builder.add_node("validator", validator_agent)
builder.add_node("learning", learning_agent)

builder.set_entry_point("classifier")

builder.add_edge("classifier", "retriever")
builder.add_edge("retriever", "decision")

builder.add_conditional_edges(
    "decision",
    lambda x: "planner" if x["decision"] == "auto_remediate" else "learning"
)

builder.add_edge("planner", "approval")
builder.add_edge("approval", "executor")
builder.add_edge("executor", "validator")

builder.add_conditional_edges(
    "validator",
    lambda x: "learning"
)

graph = builder.compile()