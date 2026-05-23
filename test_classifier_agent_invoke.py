import os
from unittest.mock import MagicMock
from app.agents.classifier_agent import classifier_agent

# Mock the state object
state = MagicMock()
state.message = "Alert: High CPU usage on production server svc-001"

try:
    print("Invoking classifier_agent...")
    result = classifier_agent(state)
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")
