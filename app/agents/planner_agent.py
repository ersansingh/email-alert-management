def planner_agent(state):
    return {
        **state,
        "remediation_plan": [
            {"step": "restart service", "tool": "shell", "action": "echo restart"}
        ]
    }