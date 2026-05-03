from typing import TypedDict, List, Dict

class AlertState(TypedDict):
    message: str
    severity: str
    alert_type: str
    service: str
    root_cause: str
    recommendation: str
    similar_incidents: List[Dict]
    decision: str
    remediation_plan: List[Dict]
    execution_status: str
    validation_status: str