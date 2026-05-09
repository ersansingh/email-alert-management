def decision_agent(state):
    if state.severity == "critical":
        return {"decision": "auto_remediate"}
    return {"decision": "notify"}