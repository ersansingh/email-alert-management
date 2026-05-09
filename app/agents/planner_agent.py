def planner_agent(state):
    return {
        "remediation_plan": [
            {"step": "restart service", "tool": "shell", "action": "echo restart"}
        ]
    }