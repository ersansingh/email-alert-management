def decision_agent(state):
    if state.get("severity") == "critical":
        return {**state, "decision": "auto_remediate"}
    return {**state, "decision": "notify"}